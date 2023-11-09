from abc import ABC

from flask import render_template, url_for, redirect, flash, request, session
from sqlalchemy.exc import OperationalError

from application.app_name.utils import frontend_login_required
from application.app_name.helpers.forms.default import DefaultForm
from application.app_name.helpers.CRUDs.frontend import ft_save_single_record, ft_get_single_record, \
    ft_get_all_records, ft_filter_record, ft_save_record, ft_update_record, ft_delete_record, \
    ft_get_all_records_paginate


def page(bp, rule, log, **options):
    def decorator(cls):
        obj = cls()

        custom_rule = rule

        log.info(f"registering {obj.TYPE} '{bp.import_name}.{cls.__name__}' as {custom_rule}")
        if obj.endpoint is None:
            obj.endpoint = bp.name

        obj.log = log

        name = getattr(obj, 'name')

        def get_page_func(obj, name):
            return frontend_login_required(getattr(obj, name), roles=obj.roles) if obj.auth else getattr(obj, name)

        # Adding the default rule
        if isinstance(obj, PaginationPage):
            log.info(f"creating rule {obj.endpoint}.data for Page {bp.import_name}.{cls.__name__}")
            bp.add_url_rule(rule=custom_rule, endpoint="data", view_func=get_page_func(obj, "index"), **options)
        else:
            page_endpoint = "index" if not name else name
            log.info(f"creating rule '{obj.endpoint}.{page_endpoint}' for Page '{bp.import_name}.{cls.__name__}'")
            bp.add_url_rule(rule=custom_rule, endpoint=page_endpoint, view_func=get_page_func(obj, "index"), **options)

        # Add additional rules based on page parent class (the order of 'if' matters)
        if isinstance(obj, FullPage):
            log.info(f"creating additional rules for Page '{bp.import_name}.{cls.__name__}'")
            bp.add_url_rule(rule=f"{custom_rule}/create", endpoint="create", view_func=get_page_func(obj, "create"),
                            **options)
            bp.add_url_rule(rule=f"{custom_rule}/<string:id>/edit", endpoint="edit",
                            view_func=get_page_func(obj, "edit"), **options)
            bp.add_url_rule(rule=f"{custom_rule}/save", endpoint="save", view_func=get_page_func(obj, "save"),
                            methods=["POST"])
            bp.add_url_rule(rule=f"{custom_rule}/<string:id>/delete", endpoint="delete",
                            view_func=get_page_func(obj, "delete"), **options)
        elif isinstance(obj, SinglePage):
            log.info(f"creating additional rules for Page '{bp.import_name}.{cls.__name__}'")
            bp.add_url_rule(rule=f"{custom_rule}/edit", endpoint="edit", view_func=get_page_func(obj, "edit"),
                            **options)
            bp.add_url_rule(rule=f"{custom_rule}/save", endpoint="save", view_func=get_page_func(obj, "save"),
                            methods=["POST"])
        elif isinstance(obj, ProfilePage):
            log.info(f"creating additional rules for Page '{bp.import_name}.{cls.__name__}'")
            bp.add_url_rule(rule=f"{custom_rule}/password", endpoint="password", view_func=get_page_func(
                obj, "password"), **options)
            bp.add_url_rule(rule=f"{custom_rule}", endpoint="submit", view_func=get_page_func(obj, "perform"),
                            methods=["POST"])
        elif isinstance(obj, FormPage):
            log.info(f"creating additional rules for Page '{bp.import_name}.{cls.__name__}'")
            bp.add_url_rule(rule=f"{custom_rule}", endpoint="submit", view_func=get_page_func(obj, "perform"),
                            methods=["POST"])
        return obj

    return decorator


class Page:
    TYPE = "Page"
    endpoint = None
    back_url = None
    template = dict(index='admin/model_page.html', form='admin/form.html')
    roles = []
    log = None
    auth = True
    name = None
    title = None
    page_title = None
    model = None
    form = DefaultForm

    def index(self):  # endpoint: <name>.index
        raise NotImplementedError

    def get_frontend_design(self):
        return ft_get_single_record(self.model)


class FormPage(Page, ABC):
    TYPE = "FormPage"

    def submit(self, form):
        raise NotImplementedError

    def perform(self):  # endpoint: <name>.submit

        form = self.form()
        if request.accept_mimetypes.provided and not request.accept_mimetypes["text/html"]:
            self.log.debug("error on submit because request.accept informed is not supported")
            flash("'accept_mimetypes' informed on request is not supported, please, verify your request", "danger")
            return redirect(url_for(f"{self.endpoint}.index"))

        data = form.validate_form()

        if data:
            self.log.debug(f"Form is valid for {self.endpoint}. Data: {data}")
            return self.submit(data)

        self.log.debug(f"validation error on {self.endpoint} form. Cause: {form.dump_errors}")
        flash(f'Invalid Data: {form.dump_errors}', "danger")
        return redirect(url_for(f"{self.endpoint}.index"))


class SinglePage(Page):
    TYPE = "SinglePage"

    create_on_none = True
    fields = []
    custom_fields = ["readonly"]
    template = dict(index='admin/list_page.html', form='admin/form.html')

    def _get_all(self):
        return ft_get_single_record(self.model)

    def index(self):
        _data = self._get_all()
        self.log.debug(f"Data found: {_data}")
        if self.create_on_none:
            try:
                if not _data:
                    self.log.debug(f"No data was found for {self.endpoint}, creating new based on default values")
                    _data = ft_save_single_record(self.model, {})
            except Exception as e:
                self.log.error("Error creating initial Defaults: {}".format(e))
                flash("Error creating with initial Defaults", "danger")
                return redirect(url_for("admin_dashboard.index"))
        if _data:
            _data = [_data]
        return render_template(self.template.get("index"), data=_data, title=self.title,
                               page_title=self.page_title, fields=self.fields, endpoint=self.endpoint,
                               custom_fields=self.custom_fields)

    def edit(self):
        self.log.debug(f"init form to edit {self.title}.{id}")
        data = self._get_all()
        self.log.debug(f"Data Found: {data}")
        if not data:
            flash('No data found to edit', 'warn')
            return redirect(url_for(self.back_url))
        form = self.form()
        form.fill_form(data)
        return render_template(
            self.template.get("form"),
            title=f"Editing {self.title}",
            page_title=self.page_title,
            action=url_for(f"{self.endpoint}.save"),
            form=form,
            back_url=url_for(self.back_url)
        )

    def save(self):
        form = self.form()
        self.log.debug(f"saving {self.endpoint}")
        data = form.validate_form()
        if data:
            try:
                self.log.debug(f"Form {self.endpoint} is valid")
                self.log.debug(f"Data validated: {data}")
                if ft_save_single_record(self.model, data):
                    flash("Saved successfully!", "success")
                    return redirect(url_for(f"{self.endpoint}.index"))
            except OperationalError as e:
                self.log.error(f"database error on {self.endpoint} save. Cause: {e}")
                flash("Something wrong happened when saving your data, try again", 'danger')
                return url_for(self.back_url)
            except Exception as e:
                self.log.error(f"error on {self.endpoint} save. Cause: {e}")
                flash("Something wrong happened when saving your data, try again", 'danger')
                return url_for(self.back_url)

        # Otherwise
        self.log.debug(f"validation error on save {self.endpoint}. Cause: {form.dump_errors}")
        flash(f'Incorrect Data: {form.dump_errors}', "danger")
        return render_template(
            self.template.get("form"),
            title=f"Editing {self.title}",
            page_title=self.page_title,
            action=url_for(f"{self.endpoint}.save"),
            form=form,
            back_url=url_for(self.back_url)
        )


class FullPage(FormPage):
    TYPE = "FullPage"

    model = None
    model_id = None
    fields = []
    additional_model = None
    custom_fields = ["copy_id"]

    def _get_all(self):
        return ft_get_all_records(self.model)

    def index(self):  # endpoint: <name>.index
        try:
            _data = self._get_all()
            self.log.debug(f"Data found: {_data}")
        except OperationalError as e:
            self.log.error(f"error when get all items from {self.endpoint}.index. Error: {e}", exc_info=True)
            flash('An error occurred while reading your data', 'danger')
            return redirect(url_for("admin_dashboard.index"))
        return render_template(self.template.get("index"), data=_data, title=self.title,
                               page_title=self.page_title, fields=self.fields, endpoint=self.endpoint,
                               custom_fields=self.custom_fields)

    def create(self):
        self.model_id = None
        return render_template(
            self.template.get("form"),
            title=f"Creating {self.title}",
            page_title=self.page_title,
            action=url_for(f"{self.endpoint}.save"),
            form=self.form(),
            back_url=url_for(self.back_url)
        )

    def edit(self, id):
        if not id:
            flash("Identifier not found, try again", "danger")
            return redirect(url_for(self.back_url))
        data = ft_filter_record(self.model, id)
        if not data:
            flash('No data found to edit', 'warn')
            return redirect(url_for(self.back_url))
        self.log.debug(f"Data found: {data}")
        self.model_id = id
        form = self.form()

        form.fill_form(data)
        return render_template(
            self.template.get("form"),
            title=f"Editing {self.title}",
            page_title=self.page_title,
            action=url_for(f"{self.endpoint}.save"),
            form=form,
            back_url=url_for(self.back_url)
        )

    def save(self):

        if "Referer" not in request.headers:
            self.log.error("The http header Referer was not found and this request will be aborted as suspicious")
            flash("'accept_mimetypes' informed on request is not supported, please, verify your request", "danger")
            return redirect(url_for(self.back_url))

        is_create = "create" in request.headers.get("Referer")
        form = self.form()
        self.log.debug(f"saving {self.endpoint}")
        data = form.validate_form()
        self.log.debug(f"saving {'new ' if is_create else 'existing '}{self.title} "
                       f"{'#' + self.model_id if not is_create and self.model_id else ''}")
        if data:
            try:
                self.log.debug(f"Form {self.endpoint} is valid")
                self.log.debug(f"Data validated: {data}")
                if self.model_id:
                    model_data = ft_update_record(self.model, self.model_id, data, additional_model=self.additional_model)
                else:
                    model_data = ft_save_record(self.model, data, additional_model=self.additional_model)
                if model_data:
                    flash("Saved with success!", "success")
                    return redirect(url_for(f"{self.endpoint}.index"))
                flash("Data not saved correctly", "danger")
                return redirect(url_for(f"{self.endpoint}.index"))
            except Exception as e:
                self.log.error(f"error on {self.endpoint} save. Cause: {e}")
                flash("An error occurred while saving your data, try again", 'danger')
                return redirect(url_for(self.back_url))

        # Otherwise
        self.log.debug("validation error on save {}. Cause: {}".format(self.endpoint, form.errors))

        title = f"Create {self.title}" if is_create else f"Editing {self.title}"
        flash(f'Incorrect data: {form.dump_errors}', "danger")
        return render_template(
            self.template.get("form"),
            title=title,
            page_title=self.page_title,
            action=url_for(f"{self.endpoint}.save"),
            form=form,
            back_url=url_for(self.back_url)
        )

    def delete(self, id):
        if not id:
            flash("Identifier not found, try again", "danger")
            return redirect(url_for(self.back_url))

        data = ft_filter_record(self.model, id)
        if not data:
            self.log.debug(f"{self.title}.{id} not found")
            flash('No data found to edit', 'warn')
            return redirect(url_for(self.back_url))
        if ft_delete_record(self.model, id):
            flash(f"{self.title} Deletado", "success")
        else:
            flash("Error on delete your data, try again", "danger")
        return redirect(url_for(f"{self.endpoint}.index"))

    def submit(self, form):
        raise NotImplementedError


class ListPage(Page):
    TYPE = "ListPage"

    model = None
    fields = []
    custom_fields = ["readonly"]
    two_fa_endpoint = None
    template = 'admin/list_page.html'

    def _get_all(self):
        return ft_get_single_record(self.model)

    def index(self):  # endpoint: <name>.index
        try:
            _data = self._get_all()
            self.log.debug(f"Data found: {_data}")
        except OperationalError as e:
            self.log.error(f"error when get all items from {self.endpoint}.index. Error: {e}", exc_info=True)
            flash('An error occurred while reading your data', 'danger')
            return redirect(url_for(self.back_url))
        return render_template(self.template, data=_data, title=self.title,
                               page_title=self.page_title, fields=self.fields, endpoint=self.endpoint,
                               custom_fields=self.custom_fields, two_fa_endpoint=self.two_fa_endpoint)


class PaginationPage(Page):
    TYPE = 'PaginationPage'
    model = None
    RECORDS_PER_PAGE: [int] = [10, 25, 50, 100]

    def _get_query(self, filter=None):

        query = self.model.query
        if filter:
            if hasattr(self.model, 'name'):
                query = query.filter_by(name=filter)
            else:
                query = query.filter_by(id=filter)
        query = query.order_by(self.model.created_at.desc())
        return query

    def index(self):

        search = request.args.get('sSearch')
        length = int(request.args.get('iDisplayLength') or 0)
        offset = int(request.args.get('iDisplayStart') or 0)

        query = self._get_query(search)
        count_data = query.count() or 0
        session['count_data'] = count_data
        query = query.offset(offset)
        query = query.limit(length)

        response = {
            'sEcho': str(request.args.get('sEcho')),
            'iTotalRecords': count_data,
            'iTotalDisplayRecords': count_data,
            'data': []
        }

        items = query.all()
        for item in items:
            response['data'].append(
                {
                    'id': item.id,
                    **item.serialized  # Using serialized to keep pattern as ListPage
                }
            )

        return response


class ProfilePage(FormPage):
    TYPE = "ProfilePage"

    profile_form = None
    password_form = None
    model = None
    template = 'admin/form.html'

    def index(self):
        try:
            identifier = session['id']
            data = ft_filter_record(self.model, identifier)
            form = self.profile_form()
            form.fill_form(data)
            return render_template(self.template, form=form,
                                   action=url_for(f"{self.endpoint}.submit"),
                                   title="Profile",
                                   page_title="Profile")
        except Exception as e:
            self.log.error(f"Error on Profile Page {self.endpoint}.index, Error: {e}")
            return redirect(url_for(f"{self.endpoint}.index"))

    def password(self):  # self.endpoint.password
        try:
            form = self.password_form()
            return render_template(self.template, form=form,
                                   action=url_for(f"{self.endpoint}.submit"),
                                   title="Password Update",
                                   page_title="Profile - Password")
        except Exception as e:
            self.log.error(f"Error on Profile Page {self.endpoint}.edit, Error: {e}")
            return redirect(url_for(f"{self.endpoint}.index"))

    def submit(self, data: dict):
        if 'username' in data.keys():
            return self.profile_submit(data)
        else:
            return self.password_submit(data)

    def profile_submit(self, data):
        identifier = session['id']
        if ft_update_record(self.model, identifier, data):
            flash("Profile updated successfully", "success")
            return redirect(url_for(f'{self.endpoint}.edit'))
        flash("Error updating profile", "danger")
        return redirect(url_for(f'{self.endpoint}.edit'))

    def password_submit(self, data):
        try:
            identifier = session['id']
            model = ft_filter_record(self.model, identifier, raw=True)
            if model.validate_password(data['old_password']):
                if ft_update_record(self.model, identifier, data):
                    flash("Password updated with success", "success")
                    return redirect(url_for(f'{self.endpoint}.password'))
                flash("Error while updating password", "danger")
                return redirect(url_for(f'{self.endpoint}.password'))
            flash("Incorrect credential", 'danger')
            return redirect(url_for(f'{self.endpoint}.password'))
        except Exception as e:
            self.log.error(f"Error on submit.password_submit. Error: {e}")
            return redirect(url_for(f"{self.endpoint}.index"))
