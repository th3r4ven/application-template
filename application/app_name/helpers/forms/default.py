

class DefaultForm:
    hide_list = ['_prefix', 'meta', '_fields', '_csrf', 'submit', 'csrf_token', 'password', 'confirm_password',
                 'form_errors']


    def fill_form(self, json_data):

        for k in json_data.keys():
            try:
                tmp = self.__getattribute__(k)
                tmp.data = json_data[k]
                self.__setattr__(k, tmp)
            except AttributeError:
                continue

    @property
    def dump_errors(self):
        data = ''
        for k, v in self.errors.items():
            if type(v) == list:
                error = '; '.join(v)
            else:
                error = v
            data += f'Field {k} - {error}; '

        return data

    def validate_form(self):
        if self.validate_on_submit():
            data = {}
            for k, v in self.__dict__.items():
                if k not in self.hide_list:
                    data[k] = v.data
            return data
        else:
            return False
