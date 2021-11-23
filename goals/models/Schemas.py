from goals.ext.migration import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = 'username', 'email'


user_share_schema = UserSchema()


class TaskSchema(ma.Schema):
    class Meta:
        fields = 'id', 'value', 'done'


task_share_schema = TaskSchema()
task_share_schemas = TaskSchema(many=True)


class GoalSchema(ma.Schema):
    talkies = ma.Nested(TaskSchema, many=True)
    class Meta:
        fields = 'id', 'description', 'price', 'talkies'


goal_share_schema = GoalSchema()
goal_share_schemas = GoalSchema(many=True)
