actual_attrs = []
attrs = ['"first_name":', '"Rahab', '"age":',
         '26', '"nick_name":', '"Scaarif Ngache"']
for idx, attr in enumerate(attrs):
    print(attr)
    if idx % 2 == 0:
        attr = attr.strip(':')
        actual_attrs.append(attr.strip('"'))
    else:
        if len(attr.split(' ')) == 1:
            actual_attrs.append(attr.strip('"'))
        else:
            actual_attrs.append(attr)
print(actual_attrs)
