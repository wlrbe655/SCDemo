from django.forms import ModelForm


class bootstrapModelForm(ModelForm):
    # 如果你有不想加输入口样式的话,把字段写在bootstrap_exclude_fields列表中
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 这两行是新加的
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性,保留原来的属性,没有属性才添加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}