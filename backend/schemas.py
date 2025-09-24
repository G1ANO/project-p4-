from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError, fields
from .database import db, ma, User, Plan, Subscription


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ("password_hash",)  

    
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)

    @validates("password")
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")


class PlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Plan
        load_instance = True


class SubscriptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription
        load_instance = True
        include_fk = True


user_schema = UserSchema()
plan_schema = PlanSchema()
plans_schema = PlanSchema(many=True)
subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)
