"""DICOM file Flywheel utils."""

import io
import logging
import random
import re
import typing as t
from datetime import datetime
from functools import partial
from pathlib import Path

import pydicom
from faker import Faker
from fw_utils import AnyFile, get_datetime, open_any

from ..utils import birthdate_to_age
from .config import UID_PREFIX

DCM_BYTE_SIG_OFFSET = 128
DCM_BYTE_SIG = b"DICM"

log = logging.getLogger(__name__)


def util_except_handler(func):
    """Decorator for unhandled exceptions within utility functions."""

    def none_if_except(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.warning(f"Exception raised when calling {func.__name__}: {e}")
            return None

    return none_if_except


def sniff_dcm(file: AnyFile) -> bool:
    """Look at file byte signature and determine if it is a DICOM."""
    with open_any(file, "rb") as fp:
        fp.seek(DCM_BYTE_SIG_OFFSET, 0)
        sig = fp.read(len(DCM_BYTE_SIG))
        return sig == DCM_BYTE_SIG


def generate_uid(
    prefix: t.Optional[str] = f"{UID_PREFIX}.2.",
    entropy_srcs: t.Optional[t.List[str]] = None,
) -> pydicom.uid.UID:
    """Return a 64 character UID which starts with the given prefix.

    Args:
        prefix (str, optional): UID prefix to use. Defaults to the Flywheel
            fw-file UID prefix for generation, "2.16.840.1.114570.2.".
        entropy_srcs (list[str], optional): List of strings to use SHA512 on
            when generating the UID characters after the prefix, making the
            result deterministic. Default is None, generating a random suffix.

    Reference:
        https://github.com/pydicom/pydicom/blob/v2.1.2/pydicom/uid.py#L382
    """
    if prefix and not prefix.endswith("."):
        prefix = f"{prefix}."
    return pydicom.uid.generate_uid(prefix=prefix, entropy_srcs=entropy_srcs)


def generate_dcm(  # noqa: PLR0913
    # TODO support keying off of pre-existing DICOM (str|path|Dataset)
    default_dict: dict | None = None,
    *,
    output_path: str | Path = "./generate_dcm",
    output_name: str = "{sub_no}_{ses_no}_{acq_no}/{SOPInstanceUID}.dcm",
    patients: int | list[dict] | None = None,
    studies: int | list[dict] | None = None,
    series: int | list[dict] | None = None,
    images: int | list[dict] | None = None,
    **default_kw,
) -> None:
    """Generate DICOM files for testing.

    Args:
        default_dict (opt): Default DICOM tags to for every instance.
        output_path (opt): Output directory path to write DICOMs to.
        output_name (opt): Filename template for naming DICOM instances.
        patients (opt): Patients to generate (count or list of tag dicts).
        studies (opt): Studies to generate (count or list of tag dicts).
        series (opt): Series to generate (count or list of tag dicts).
        images (opt): Instances to generate (count or list of tag dicts).
        **default_kw (opt): Default DICOM tags as keywords for every instance.
    """

    def auto(name: str, spec: int | list[dict] | None) -> list[dict]:
        err = f"generate_dcm(): invalid arg for {name}: {type(spec)}({spec})"
        if spec is None:
            return [{}]
        if isinstance(spec, int):
            if spec <= 0:  # pragma: no cover
                raise ValueError(err)
            return [{} for _ in range(spec)]
        if isinstance(spec, list):
            return spec
        raise TypeError(err)  # pragma: no cover

    subs = auto("patients", patients)
    sess = auto("studies", studies)
    acqs = auto("series", series)
    imgs = auto("images", images)
    faker = Faker()
    uid_gen = generate_uid
    dob_gen = partial(faker.date_between, "-75y", "-20y")
    sex_gen = partial(random.choice, ["M", "F"])
    name_gen = {"M": faker.name_male, "F": faker.name_female}
    defaults = (default_dict or {}) | default_kw
    for sub_no, sub in enumerate(subs, start=1):
        sub_prefix = f"{UID_PREFIX}.2.{sub_no}"
        sub = defaults | sub
        sub.setdefault("PatientID", f"subject_{sub_no:03d}")
        sex = sub.setdefault("PatientSex", sex_gen())
        sub.setdefault("PatientName", name_gen.get(sex, faker.name_nonbinary)())
        sub.setdefault("PatientBirthDate", dob_gen().strftime("%Y%m%d"))
        for ses_no, ses in enumerate(sess, start=1):
            ses_prefix = f"{sub_prefix}.{ses_no}"
            ses = sub | ses
            ses.setdefault("StudyInstanceUID", uid_gen(f"{ses_prefix}.0.0"))
            ses.setdefault("StudyDescription", f"session_{ses_no:03d}")
            for acq_no, acq in enumerate(acqs, start=1):
                acq_prefix = f"{ses_prefix}.{acq_no}"
                acq = ses | acq
                acq.setdefault("SeriesInstanceUID", uid_gen(f"{acq_prefix}.0"))
                acq.setdefault("SeriesDescription", f"acquisition_{acq_no:03d}")
                for img_no, img in enumerate(imgs, start=1):
                    img_prefix = f"{acq_prefix}.{img_no}"
                    img = acq | img
                    img.setdefault("Modality", "MR")
                    img.setdefault("SOPClassUID", "1.2.840.10008.5.1.4.1.1.4")
                    img.setdefault("SOPInstanceUID", uid_gen(img_prefix))
                    path = Path(output_path) / output_name.format(**locals(), **img)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(create_dcm(**img).getvalue())


def create_dcm(preamble=None, file_meta=None, **dcmdict) -> io.BytesIO:
    """Create and return a DICOM file as BytesIO object from a tag dict."""
    dcm = io.BytesIO()
    dataset = pydicom.FileDataset(dcm, create_dataset(**dcmdict))
    dataset.preamble = preamble or b"\x00" * 128
    dataset.file_meta = pydicom.dataset.FileMetaDataset()
    update_dataset(dataset.file_meta, file_meta)
    pydicom.dcmwrite(dcm, dataset, write_like_original=bool(file_meta))
    dcm.seek(0)
    return dcm


def create_dataset(**dcmdict) -> pydicom.Dataset:
    """Create and return a pydicom.Dataset from a simple tag dictionary."""
    dataset = pydicom.Dataset()
    update_dataset(dataset, dcmdict)
    return dataset


def update_dataset(dataset: pydicom.Dataset, dcmdict: dict) -> None:
    """Add dataelements to a dataset from the given tag dictionary."""
    dcmdict = dcmdict or {}
    for key, value in dcmdict.items():
        # if value is a list/tuple, it's expected to be a (VR,value) pair
        if isinstance(value, (list, tuple)):
            VR, value = value
        # otherwise it's just the value, so get the VR from the datadict
        else:
            VR = pydicom.datadict.dictionary_VR(key)
        dataset.add_new(key, VR, value)


@util_except_handler
def parse_datetime_str(value: str) -> t.Optional[datetime]:
    """Parse datetime string.

    Args:
        value (str): DICOM DT formatted timestamp: YYYYMMDDHHMMSS.FFFFFF&ZZXX
            The year is required, but everything else has defaults:
            month=day=1, hour=12, minute=second=microsecond=0

    Reference:
        http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """
    try:
        dt_obj = get_datetime(f"{value[:8]} {value[8:]}")
    except ValueError:
        return None
    except OverflowError:
        # If datetime str is at the minimum allowed by datetime, the tz offset
        # can push the value out of bounds for timezones west of UTC.
        if re.search(r"[+-]\d{4}$", value):
            dt_obj = get_datetime(f"{value[:8]} {value[8:-5]}")
        else:
            # If there isn't a tz offset, raise just in case
            raise OverflowError
    if len(value) < 10:
        dt_obj = dt_obj.replace(hour=12)
    return dt_obj


def get_timestamp(
    dcm: t.Mapping[str, t.Any], tag_prefix: str = "Series"
) -> t.Optional[datetime]:
    """Get timestamp from Study-, Series- or Acquisition Date/Time tags.

    Args:
        dcm (dicom.DICOM): DICOM instance
        tag_prefix (str, optional): Date/time tag prefix: Study|Series|Acquisition
            Defaults to "Series".

    Reference of DA/TM/DT VR types:
        http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """
    assert tag_prefix in {"Study", "Series", "Acquisition"}
    datetime_str = ""
    if tag_prefix == "Acquisition" and dcm.get("AcquisitionDateTime"):
        datetime_str = dcm["AcquisitionDateTime"]
    elif dcm.get(f"{tag_prefix}Date"):
        date = dcm.get(f"{tag_prefix}Date")
        time = dcm.get(f"{tag_prefix}Time") or ""
        datetime_str = f"{date}{time}"
    elif tag_prefix != "Acquisition" and get_uid_timestamp(dcm, tag_prefix):
        datetime_str = t.cast(str, get_uid_timestamp(dcm, tag_prefix))
    else:
        return None
    # get offset from TimezoneOffsetFromUTC if not in the datetime string yet
    if not re.match(r"[+-]\d{4}$", datetime_str):
        offset = dcm.get("TimezoneOffsetFromUTC", "")
        if offset and offset[0] not in "+-":
            # make sure offset is sign-prefixed (sign optional in this tag)
            offset = f"+{offset}"
        datetime_str = f"{datetime_str}{offset}"
    return parse_datetime_str(datetime_str)


def get_uid_timestamp(
    dcm: t.Mapping[str, t.Any], tag_prefix: str = "Series"
) -> t.Optional[str]:
    """Attempt to get a timestamp string from the Study- or Series UID."""
    assert tag_prefix in {"Study", "Series"}
    uid = dcm.get(f"{tag_prefix}InstanceUID") or ""
    uid_timestamp_re = r"\d+(\.\d+)*\.(?P<timestamp>(19|20)\d{12,})(\.\d+)*"
    match = re.match(uid_timestamp_re, uid)
    if match:
        return match.group("timestamp")[:14]
    return None


@util_except_handler
def get_operators_name(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Get operators name, collapsing to string if multiple."""
    res = dcm.get("OperatorsName")
    if res and isinstance(res, (pydicom.multival.MultiValue, list, tuple)):
        names = []
        for name in res:
            f_name, l_name = parse_person_name(name)
            names.append(f"{f_name or ''} {l_name or ''}".strip())
        return ", ".join(names)
    return res


def get_patient_name(
    dcm: t.Mapping[str, t.Any],
) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """Return firstname, lastname tuple from a DICOM."""
    name = dcm.get("PatientName")
    if not name:
        return None, None
    return parse_person_name(name)


def parse_person_name(name: str) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """Return firstname, lastname tuple from a PN string."""
    if "^" in name:
        lastname, _, firstname = name.partition("^")
    else:
        firstname, _, lastname = name.rpartition(" ")
    return (firstname.strip().title() or None, lastname.strip().title() or None)


@util_except_handler
def get_session_age(dcm: t.Mapping[str, t.Any]) -> t.Optional[int]:
    """Return patient age in seconds."""
    if dcm.get("PatientAge"):
        age_str = dcm.get("PatientAge", "")
        match = re.match(r"(?P<value>[0-9]+)(?P<scale>[dwmyDWMY])?", age_str)
        if match:
            # convert to days
            conversion = {"Y": 365.25, "M": 30, "W": 7, "D": 1}
            value = match.group("value")
            scale = (match.group("scale") or "Y").upper()
            return int(int(value) * conversion[scale] * 86400)

    birth_date = parse_datetime_str(dcm.get("PatientBirthDate", ""))  # type: ignore
    acq_timestamp = get_acquisition_timestamp(dcm)
    if not (birth_date and acq_timestamp):
        return None

    return birthdate_to_age(birth_date, acq_timestamp)


@util_except_handler
def get_session_label(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return session label.

    1. StudyDescription
    2. Session timestamp (YYYY-mm-ddTHH-MM-SS)
    3. StudyInstanceUID
    """
    label = dcm.get("StudyDescription")
    if not label and (ts := get_session_timestamp(dcm)):
        label = ts.strftime("%Y-%m-%dT%H-%M-%S")
    return label or dcm.get("StudyInstanceUID")


@util_except_handler
def get_session_timestamp(dcm: t.Mapping[str, t.Any]) -> t.Optional[datetime]:
    """Return session timestamp.

    1. StudyDate + Time
    2. StudyInstanceUID
    3. SeriesDate + Time
    4. SeriesInstanceUID
    5. AcquisitionDateTime
    6. AcquisitionDate + Time
    """
    return (
        get_timestamp(dcm, "Study")
        or get_timestamp(dcm, "Series")
        or get_timestamp(dcm, "Acquisition")
    )


@util_except_handler
def get_acquisition_uid(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return acquisition UID."""
    # TODO GE: separate UID per AcquisitionNumber
    return dcm.get("SeriesInstanceUID")


@util_except_handler
def get_acquisition_label(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return acquisition label.

    1. [SeriesNumber - ]SeriesDescription
    2. [SeriesNumber - ]ProtocolName
    3. [SeriesNumber - ]Acquisition timestamp (YYYY-mm-ddTHH-MM-SS)
    4. [SeriesNumber - ]SeriesInstanceUID
    """
    label = dcm.get("SeriesDescription") or dcm.get("ProtocolName")
    if not label and (ts := get_acquisition_timestamp(dcm)):
        label = ts.strftime("%Y-%m-%dT%H-%M-%S")
    label = label or dcm.get("SeriesInstanceUID")
    if label and (series_number := dcm.get("SeriesNumber")):
        label = f"{series_number} - {label}"
    return label


@util_except_handler
def get_acquisition_timestamp(dcm: t.Mapping[str, t.Any]) -> t.Optional[datetime]:
    """Return acquisition timestamp.

    1. AcquisitionDateTime
    2. AcquisitionDate + Time
    3. SeriesDate + Time
    4. SeriesInstanceUID
    5. StudyDate + Time
    6. StudyInstanceUID
    """
    return (
        get_timestamp(dcm, "Acquisition")
        or get_timestamp(dcm, "Series")
        or get_timestamp(dcm, "Study")
    )


def get_instance_filename(dcm: t.Mapping[str, t.Any]) -> str:
    """Return recommended DICOM instance filename."""
    instance_uid = dcm.get("SOPInstanceUID")
    modality = dcm.get("Modality") or "NA"
    return f"{instance_uid}.{modality}.dcm"
