from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import User, Plan, Subscription

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)
        include_fk = True

    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)


class PlanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plan
        load_instance = True


class SubscriptionSchema(SQLAlchemyAutoSchema):
    plan_name = fields.Method("get_plan_name")

    class Meta:
        model = Subscription
        load_instance = True
        include_fk = True

    def get_plan_name(self, obj):
        return obj.plan.name if obj.plan else None
