from terraform_base_action_test_case import TerraformBaseActionTestCase
from destroy import Destroy
from dda_python_terraform import IsFlagged
import mock


class DestroyTestCase(TerraformBaseActionTestCase):
    __test__ = True
    action_cls = Destroy

    def test_init(self):
        action = self.get_action_instance({})
        self.assertIsInstance(action, Destroy)

    @mock.patch("lib.action.TerraformBaseAction.set_semantic_version")
    @mock.patch("lib.action.TerraformBaseAction.check_result")
    @mock.patch("lib.action.Terraform.destroy")
    def test_run(self, mock_destroy, mock_check_result, mock_version):
        action = self.get_action_instance({})
        # Declare test input values
        test_plan_path = "/terraform"
        test_state_file = "/terraform/terraform.tfstate"
        test_target_resources = ["module.resource"]
        test_terraform_exec = "/usr/bin/terraform"
        test_variable_dict = {'key1': 'value1', 'key2': 'value2'}
        test_variable_files = ["/terraform/test.tfvars"]
        test_env_variable_dict = {'key1': 'value1', 'key2': 'value2'}

        # Declare test Terraform.plan return values
        test_return_code = 0
        test_stdout = "Object successfully destroyed!"
        test_stderr = ""

        mock_version.return_value = '1.1.1'
        mock_destroy.return_value = test_return_code, test_stdout, test_stderr

        expected_result = "result"
        mock_check_result.return_value = expected_result

        # Execute the run function
        result = action.run(test_plan_path, test_state_file, test_target_resources,
                            test_terraform_exec, test_variable_dict, test_variable_files,
                            test_env_variable_dict)

        # Verify the results
        self.assertEqual(result, expected_result)
        self.assertEqual(action.terraform.targets, test_target_resources)
        self.assertEqual(action.terraform.terraform_bin_path, test_terraform_exec)
        self.assertEqual(action.set_env_variable_dict(test_env_variable_dict), True)
        mock_destroy.assert_called_with(
            var_file=test_variable_files,
            var=test_variable_dict,
            state=test_state_file,
            force=IsFlagged,
            capture_output=False,
            raise_on_error=False
        )
        mock_check_result.assert_called_with(
            test_return_code,
            test_stdout,
            test_stderr,
            return_output=True
        )
