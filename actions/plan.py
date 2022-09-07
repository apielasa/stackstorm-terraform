import os
from lib import action


class Plan(action.TerraformBaseAction):
    def run(self, plan_path, state_file_path, target_resources, terraform_exec,
            variable_dict, variable_files):
        """
        Plan the changes required to reach the desired state of the configuration

        Args:
        - plan_path: path of the Terraform files
        - state_file_path: path of the Terraform state file
        - target_resources: list of resources to target from the configuration
        - terraform_exec: path of the Terraform bin
        - variable_dict: dictionary of Terraform variables that will overwrite the
            variable files if both are declared
        - variable_files: array of Terraform variable files

        Returns:
        - dict: Terraform output command output
        """
        os.chdir(plan_path)
        self.terraform.state = state_file_path
        self.terraform.targets = target_resources
        self.terraform.terraform_bin_path = terraform_exec
        self.terraform.var_file = variable_files
        self.terraform.variables = variable_dict
        self.set_semantic_version()
        return_code, stdout, stderr = self.terraform.plan(plan_path,
        capture_output=False,
        raise_on_error=False)

        return self.check_result(
            return_code,
            stdout,
            stderr,
            return_output=True,
            valid_return_codes=[0, 2]
        )
