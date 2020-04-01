from voluptuous import (
    Required,
    Schema,
    Length)


class ValidatorSchema(Schema):
    pass


checkblack_validator = ValidatorSchema({
    Required('nik'): Length(min=16, max=16, msg='please check the NIK format'),
    Required('name'): Length(min=1, max=50, msg='please check the NAME format'),
    Required('mobile_no'): Length(min=5, max=16,msg='please check the MOBILE_NO format')
})


nik_multi_platform_validator = ValidatorSchema({
    Required('nik'): Length(min=16, max=16,msg='please check the NIK format')
})


mobile_multi_platform_validator = ValidatorSchema({
    Required('mobile_no'): Length(min=5, max=16,msg='please check the MOBILE_NO format')
})


nik_check_validator = ValidatorSchema({
    Required('nik'): Length(min=16, max=16,msg='please check the NIK format'),
    Required('name'): Length(min=1, max=50,msg='please check the NAME format')
})

mobile_online_validator = ValidatorSchema({
    Required('mobile_no'): Length(min=5, max=16,msg='please check the MOBILE_NO format')
})


nik_mobile_check_validator = ValidatorSchema({
    Required('nik'): Length(min=16, max=16,msg='please check the NIK format'),
    Required('mobile_no'): Length(min=5, max=20,msg='please check the MOBILE NO format')
})


user_validator = ValidatorSchema({
    Required('username'): Length(min=3, max=10,msg='please check the username format, the longth is from 3 to 10'),
    Required('password'): Length(min=6, max=10,msg='please check the PASSWORD format, the longth is from 6 to 10')
})
