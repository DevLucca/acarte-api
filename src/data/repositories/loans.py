import calendar
from pony import orm
from uuid import UUID
from uuid import uuid4
from datetime import date, datetime

from domain.dtos.users import UserDTO
from domain.dtos.loans import LoanDTO

from data.repositories import BaseRepository
from data.repositories.users import UserRepository
from data.repositories.students import StudentRepository
from data.repositories.instruments import InstrumentRepository
from data.entities.loans import LoansEntity

class LoanRepository(BaseRepository):
    Entity: type[LoansEntity]
    DTO: type[LoanDTO]

    def __init__(self) -> None:
        self.Entity = LoansEntity
        self.DTO = LoanDTO

    def _get_db_obj(self, id):
        try:
            if type(id) == str or type(id) == UUID:
                db_obj = (
                    orm.select(
                        (loan, stud, inst) for loan in self.Entity for inst in loan.instruments for stud in loan.student
                            if loan.uuid == id
                    )
                )
            else:
                db_obj = (
                    orm.select(
                        (loan, stud, inst) for loan in self.Entity for inst in loan.instruments for stud in loan.student
                            if loan.id == id
                    )
                )
            assert list(db_obj)
            return list(db_obj)
        except (orm.ObjectNotFound, AssertionError):
            raise self.Exceptions.DoesNotExist

    def query(self, **kwargs):
        filters = self._clean_filter_args(kwargs)
        today = date.today()
        db_query = (
            orm.select(
                (loan, stud, inst) for loan in self.Entity for inst in loan.instruments for stud in loan.student
                       if filters.get('lented_at', date(today.year, today.month, 1)) <= loan.lented_at
                       and filters.get('returned_at', date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])) >= orm.coalesce(loan.returned_at, date.today())
            )
        )
        to_be_dto = []
        loan_list = {}
        for db_obj in db_query:
            loan, stud, inst = db_obj
            stud = stud.to_dict()
            inst = inst.to_dict()
            del stud['updated_by']
            del inst['updated_by']
            if loan_id := loan_list.get(loan.id, None):
                loan_id['instruments'].append(inst)
            else:
                loan = loan.to_dict(related_objects=True)
                loan['updated_by'] = self._get_related_object(loan.get('updated_by'), UserRepository(), UserDTO)
                loan['student'] = stud
                loan['instruments'] = [inst]
                loan_list[loan['id']] = loan

        inst_uuid = filters.get('instrument_uuid')
        stud_uuid = filters.get('student_uuid')
        for _, v in loan_list.items():
            if (inst_uuid is not None) or (stud_uuid is not None):
                if inst_uuid in [instr['uuid'] for instr in v['instruments']] or stud_uuid == v['student']['uuid']:
                    to_be_dto.append(self.DTO(**v))
                    continue
            else:
                to_be_dto.append(self.DTO(**v))

        return to_be_dto
    
    def get(self, id: any):
        db_objs = self._get_db_obj(id)
        to_be_loan = {}
        for db_obj in db_objs:
            loan, stud, inst = db_obj
            stud = stud.to_dict()
            inst = inst.to_dict()
            del stud['updated_by']
            del inst['updated_by']
            if loan_id := to_be_loan:
                loan_id['instruments'].append(inst)
            else:
                loan = loan.to_dict(related_objects=True)
                loan['updated_by'] = self._get_related_object(loan.get('updated_by'), UserRepository(), UserDTO)
                loan['student'] = stud
                loan['instruments'] = [inst]
                to_be_loan = loan
        return self.DTO(**to_be_loan)

    def create(self, dto):
        try:
            dto.uuid = uuid4()
            dto.created_at = datetime.now()
            dto.lented_at = datetime.now()
            user = dto.updated_by
            instruments = dto.instruments
            student = dto.student
            del dto.updated_by
            del dto.instruments
            del dto.student
            db_obj = self.Entity(
                **dto.dict(), 
                instruments=[InstrumentRepository()._get_db_obj(inst.uuid) for inst in instruments], 
                student=StudentRepository()._get_db_obj(student.uuid),
                updated_by=UserRepository()._get_db_obj(user.uuid)
            )
            orm.commit()
            db_objs = self._get_db_obj(db_obj.uuid)
            to_be_loan = {}
            for db_obj in db_objs:
                loan, stud, inst = db_obj
                stud = stud.to_dict()
                inst = inst.to_dict()
                del stud['updated_by']
                del inst['updated_by']
                if loan_id := to_be_loan:
                    loan_id['instruments'].append(inst)
                else:
                    loan = loan.to_dict(related_objects=True)
                    loan['updated_by'] = self._get_related_object(loan.get('updated_by'), UserRepository(), UserDTO)
                    loan['student'] = stud
                    loan['instruments'] = [inst]
                    to_be_loan = loan
            return self.DTO(**to_be_loan)
        except orm.core.TransactionIntegrityError:
            raise self.Exceptions.AlreadyExists

    def save(self, dto):
        db_objs = self._get_db_obj(dto.uuid)
        dto.updated_at = datetime.now()
        dto.returned_at = datetime.now()
        user = dto.updated_by
        del dto.updated_by
        del dto.instruments
        del dto.student
        db_objs[0][0].set(**dto.dict(), updated_by=UserRepository()._get_db_obj(user.uuid))
        orm.commit()
        to_be_loan = {}
        for db_obj in db_objs:
            loan, stud, inst = db_obj
            stud = stud.to_dict()
            inst = inst.to_dict()
            del stud['updated_by']
            del inst['updated_by']
            if loan_id := to_be_loan:
                loan_id['instruments'].append(inst)
            else:
                loan = loan.to_dict(related_objects=True)
                loan['updated_by'] = self._get_related_object(loan.get('updated_by'), UserRepository(), UserDTO)
                loan['student'] = stud
                loan['instruments'] = [inst]
                to_be_loan = loan
        return self.DTO(**to_be_loan)
