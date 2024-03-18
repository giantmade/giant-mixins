from mixins.fields import DateField


class TestDateField:

    def test_date_field_type(self):
        start_date = DateField()
        html = start_date.widget.render('start_field', '2024-03-15')
        assert 'type="date"' in html