# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )

    # def resolve_name(self, info, extra1, extra2):
    #     return self.name.split(' ')[0]

class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_employees = SQLAlchemyConnectionField(EmployeeConnections)

    all_departments = SQLAlchemyConnectionField(DepartmentConnection)


class CreateDepartment(graphene.Mutation):

    #Input Arguments
    class Input:
        name = graphene.String()

    #Return Values
    name = graphene.String()

    #Performs work of mutation
    @classmethod
    def mutate(cls, _, args, context,info):
        newDepartment = DepartmentModel(name=args.get('name'))
        db_session.add(newDepartment)
        db_session.commit()

        return CreateDepartment(name=args.get('name'))

class Mutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)