import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.appointments import Appointments, AppointmentStatuses
from app.repositories.db_appointments_repo import AppointmentsRepo
from app.repositories.trainers_repo import TrainersRepo
from app.settings import settings

sleep(2)


@pytest.fixture()
def appointment_repo() -> AppointmentsRepo:
    repo = AppointmentsRepo()
    return repo


@pytest.fixture(scope='session')
def trainers_repo() -> TrainersRepo:
    return TrainersRepo()


@pytest.fixture(scope='session')
def first_appointment() -> Appointments:
    return Appointments(id=uuid4(), type='type', creation_date=datetime.now(),appointment_date=datetime.now(), status=AppointmentStatuses.CREATED)


@pytest.fixture(scope='session')
def second_appointment() -> Appointments:
    return Appointments(id=uuid4(), type='type', creation_date=datetime.now(),appointment_date=datetime.now(), status=AppointmentStatuses.CREATED)


def test_empty_list(appointment_repo: AppointmentsRepo) -> None:
    assert appointment_repo.get_appointment() == []


def test_add_first_appointment(first_appointment: Appointments, appointment_repo: AppointmentsRepo) -> None:
    assert appointment_repo.create_appointment(first_appointment) == first_appointment


def test_add_first_appointment_repeat(first_appointment: Appointments, appointment_repo: AppointmentsRepo) -> None:
    with pytest.raises(KeyError):
        appointment_repo.create_appointment(first_appointment)


def test_get_appointment_by_id(first_appointment: Appointments, appointment_repo: AppointmentsRepo) -> None:
    assert appointment_repo.get_appointment_by_id(
        first_appointment.id) == first_appointment


def test_get_appointment_by_id_error(appointment_repo: AppointmentsRepo) -> None:
    with pytest.raises(KeyError):
        appointment_repo.get_appointment_by_id(uuid4())


def test_add_second_appointment(first_appointment: Appointments, second_appointment: Appointments, appointment_repo: AppointmentsRepo) -> None:
    assert appointment_repo.create_appointment(second_appointment) == second_appointment
    appointments = appointment_repo.get_appointment()
    assert len(appointments) == 2
    assert appointments[0] == first_appointment
    assert appointments[1] == second_appointment


def test_set_status(first_appointment: Appointments, appointment_repo: AppointmentsRepo) -> None:
    first_appointment.status = AppointmentStatuses.ACTIVATED
    assert appointment_repo.set_status(
        first_appointment).status == first_appointment.status

    first_appointment.status = AppointmentStatuses.CANCELED
    assert appointment_repo.set_status(
        first_appointment).status == first_appointment.status

    first_appointment.status = AppointmentStatuses.DONE
    assert appointment_repo.set_status(
        first_appointment).status == first_appointment.status

    first_appointment.status = AppointmentStatuses.CREATED
    assert appointment_repo.set_status(
        first_appointment).status == first_appointment.status


def test_set_trainers(first_appointment: Appointments, trainers_repo: TrainersRepo, appointment_repo: AppointmentsRepo) -> None:
    first_appointment.trainer = trainers_repo.get_trainer()[0]
    assert appointment_repo.set_trainer(
        first_appointment).trainer == trainers_repo.get_trainer()[0]


def test_change_trainers(first_appointment: Appointments, trainers_repo: TrainersRepo, appointment_repo: AppointmentsRepo) -> None:
    first_appointment.trainer = trainers_repo.get_trainer()[1]
    assert appointment_repo.set_trainer(
        first_appointment).trainer == trainers_repo.get_trainer()[1]