from ..base import APITest

URL = '/v1/claims/'


class ClaimListPostGeneralSuccessTest(APITest):
    def setUp(self):
        super(ClaimListPostGeneralSuccessTest, self).setUp()
        self.post_data = {
            'resource': 'post-resource',
            'timeout': 0.010,
        }
        self.response = self.post(URL, self.post_data)

    def test_should_set_valid_location_header(self):
        url = self.response.headers['Location']
        response = self.get(url)
        self.assertEqual(200, response.status_code)

# TODO
#    def test_should_set_user_provided_data(self):
#        pass

# TODO
#    def test_should_set_automatic_fields(self):
#        pass


class ClaimListPostSuccessWithoutContentionTest(APITest):
    def setUp(self):
        super(ClaimListPostSuccessWithoutContentionTest, self).setUp()
        self.post_data = {
            'resource': 'post-resource',
            'timeout': 0.010,
        }
        self.response = self.post(URL, self.post_data)

    def test_should_return_201(self):
        self.assertEqual(201, self.response.status_code)

    def test_should_set_status_to_active(self):
        url = self.response.headers['Location']
        response = self.get(url)
        self.assertEqual('active', response.DATA['status'])

# TODO
#    def test_should_set_ttl_to_timeout(self):
#        pass


class ClaimListPostSuccessWithContentionTest(APITest):
    def setUp(self):
        super(ClaimListPostSuccessWithContentionTest, self).setUp()
        self.post_data = {
            'resource': 'post-resource',
            'timeout': 0.010,
        }
        self.first_response = self.post(URL, self.post_data)
        self.second_response = self.post(URL, self.post_data)

    def test_should_return_202(self):
        self.assertEqual(202, self.second_response.status_code)

    def test_should_set_status_to_waiting(self):
        self.assertEqual('waiting', self.second_response.DATA['status'])


class ClaimListPostErrorTest(APITest):
    def test_missing_mandatory_parameters_should_return_400(self):
        no_params_response = self.post(URL, data={})
        self.assertEqual(400, no_params_response.status_code)
#        self.assertIn('resource', no_params_response.data)
#        self.assertIn('timeout', no_params_response.data)

        no_resource_response = self.post(URL, {'timeout': 1.2})
        self.assertEqual(400, no_resource_response.status_code)
#        self.assertIn('resource', no_resource_response.data)

        no_timeout_response = self.post(URL, {'resource': 'foo'})
        self.assertEqual(400, no_timeout_response.status_code)
#        self.assertIn('timeout', no_timeout_response.data)

    def test_invalid_parameter_values_should_return_400(self):
        empty_resource_response = self.post(URL, {
            'resource': '',
            'timeout': 1.2,
        })
        self.assertEqual(400, empty_resource_response.status_code)
#        self.assertIn('resource', empty_resource_response.data)

        negative_timeout_response = self.post(URL, {
            'resource': 'foo',
            'timeout': -1.2,
        })
        self.assertEqual(400, negative_timeout_response.status_code)
#        self.assertIn('timeout', negative_timeout_response.data)

# TODO
#    def test_unknown_parameters_should_return_400(self):
#        unknown_param_response = self.post(URL, data={
#            'resource': 'foo',
#            'timeout': 1.2,
#            'unknown_param': 'enigma',
#        })
#        self.assertEqual(400, unknown_param_response.status_code)
#        self.assertIn('unknown_param', unknown_param_response.data)
