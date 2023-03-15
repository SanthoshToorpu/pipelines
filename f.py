from kfp import dsl


@dsl.container_component
def comp():
    return dsl.ContainerSpec(
        image='python:3.7',
        command=[
            "sh", "-c",
            "\nif ! [ -x \"$(command -v pip)\" ]; then\n    python3 -m ensurepip || python3 -m ensurepip --user || apt-get install python3-pip\nfi\n\nPIP_DISABLE_PIP_VERSION_CHECK=1 python3 -m pip install --quiet     --no-warn-script-location 'kfp==1.8.18' && \"$0\" \"$@\"\n",
            "sh", "-ec",
            "program_path=$(mktemp -d)\nprintf \"%s\" \"$0\" > \"$program_path/ephemeral_component.py\"\npython3 -m kfp.v2.components.executor_main                         --component_module_path                         \"$program_path/ephemeral_component.py\"                         \"$@\"\n",
            "\nimport kfp\nfrom kfp.v2 import dsl\nfrom kfp.v2.dsl import *\nfrom typing import *\n\ndef virtual_component(runtime_params:dict,module_params:dict,project_params:dict):\n    import os, sys\n    import subprocess\n    from datetime import datetime\n\n    startTime = datetime.now()\n    def main() -> None:\n        try:\n            print(\"INFO: Main script execution starting...\")\n\n            print(\"######## Access Runtime Parameters ###########\")\n\n            etl_config = runtime_params['etl_config']\n            project_name = runtime_params['project_name']\n            cmd_config_file = runtime_params['cmd_config_file']\n            parameters_file_path = runtime_params['parameters_file_path']\n            request_id = runtime_params['request_id']\n\n            print(\"etl_config: \",etl_config)\n            print(\"project_name: \",project_name)\n            print(\"cmd_config_file: \",cmd_config_file)\n            print(\"parameters_file_path: \",parameters_file_path)\n            print(\"request_id:\",request_id)\n\n            cmd = f\"python /app/mt_attributes_rca_main.py {etl_config} {project_name} {cmd_config_file} {parameters_file_path} {request_id}\"\n            #p = subprocess.call(cmd)\n            print(\"command: \",cmd)\n            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n            out, err = p.communicate()\n            output = out.decode('UTF-8').strip()\n            error = err.decode('UTF-8').strip()\n            print(\"Subprocess output: returncode: %d output: %s error: %s\" % (p.returncode, output, error ))\n            #p = subprocess.run( cmd, capture_output=True, text=True,).stdout\n\n            print(\"INFO: Main script execution completed\")\n\n        except Exception as e:\n            print(\"ERROR: Main Script Execution Failed\")\n            raise Exception(\"ERROR: Main Script Execution \\n {}\".format(str(e)))\n            sys.exit(1)\n\n        finally:\n            print(\"INFO: Time Elapsed: \",datetime.now() - startTime,\" Seconds\")\n\n    main()\n\n"
        ],
        args=[
            "--executor_input",
            "{\"inputs\":{\"parameterValues\":{\"module_params\":\"{\\\"pipeline_spec_uri\\\": \\\"json_folder/pipeline_mt_attributes.json\\\", \\\"display_name\\\": \\\"mt-attr-rca-vi-kfp-pipeline\\\", \\\"bucket_id2\\\": \\\"cjmccarthy-kfp-default-bucket\\\", \\\"region2\\\": \\\"us-central1\\\"}\",\"project_params\":\"{\\\"project_id\\\": \\\"gdw-dev-dpmuptick\\\", \\\"bucket_id\\\": \\\"gdw-dev-dpmuptick-default\\\", \\\"container_credential_file\\\": \\\"/app/key.json\\\", \\\"airflow_credential_file\\\": \\\"/home/jupyter/managed_pipelines/dpm_uptick_rca/key.json\\\", \\\"region\\\": \\\"us-west1\\\", \\\"pipeline_root\\\": \\\"gs://cjmccarthy-kfp-default-bucket/kubeflow\\\", \\\"network\\\": \\\"projects/993472749337/global/networks/vpc-micron-core-01\\\"}\",\"runtime_params\":\"{\\\"etl_config\\\": \\\"gs://gdw-dev-dpmuptick-default/scripts/config/mt_attr_etl_job_config.json\\\", \\\"project_name\\\": \\\"gdw-dev-dpmuptick\\\", \\\"cmd_config_file\\\": \\\"gs://gdw-dev-dpmuptick-default/scripts/config/ssh_onprem_cmds_v1.json\\\", \\\"parameters_file_path\\\": \\\"gs://cjmccarthy-kfp-default-bucket/parameters/parameter_Z32D_mtsums_both_QMON-ver_ww37_38_39_40_RPP_fab15_15_202301261754.json\\\", \\\"request_id\\\": \\\"Z32D_mtsums_both_QMON-all_ww29_28_CPP_fab15_15_202301170924\\\", \\\"jsonfileloc\\\": \\\"/home/jupyter/managed_pipelines/dpm_uptick_rca/gdw-dev-dpmuptick_config.json\\\"}\"},\"parameters\":{\"module_params\":{\"stringValue\":\"{\\\"pipeline_spec_uri\\\": \\\"json_folder/pipeline_mt_attributes.json\\\", \\\"display_name\\\": \\\"mt-attr-rca-vi-kfp-pipeline\\\", \\\"bucket_id2\\\": \\\"cjmccarthy-kfp-default-bucket\\\", \\\"region2\\\": \\\"us-central1\\\"}\"},\"project_params\":{\"stringValue\":\"{\\\"project_id\\\": \\\"gdw-dev-dpmuptick\\\", \\\"bucket_id\\\": \\\"gdw-dev-dpmuptick-default\\\", \\\"container_credential_file\\\": \\\"/app/key.json\\\", \\\"airflow_credential_file\\\": \\\"/home/jupyter/managed_pipelines/dpm_uptick_rca/key.json\\\", \\\"region\\\": \\\"us-west1\\\", \\\"pipeline_root\\\": \\\"gs://cjmccarthy-kfp-default-bucket/kubeflow\\\", \\\"network\\\": \\\"projects/993472749337/global/networks/vpc-micron-core-01\\\"}\"},\"runtime_params\":{\"stringValue\":\"{\\\"etl_config\\\": \\\"gs://gdw-dev-dpmuptick-default/scripts/config/mt_attr_etl_job_config.json\\\", \\\"project_name\\\": \\\"gdw-dev-dpmuptick\\\", \\\"cmd_config_file\\\": \\\"gs://gdw-dev-dpmuptick-default/scripts/config/ssh_onprem_cmds_v1.json\\\", \\\"parameters_file_path\\\": \\\"gs://cjmccarthy-kfp-default-bucket/parameters/parameter_Z32D_mtsums_both_QMON-ver_ww37_38_39_40_RPP_fab15_15_202301261754.json\\\", \\\"request_id\\\": \\\"Z32D_mtsums_both_QMON-all_ww29_28_CPP_fab15_15_202301170924\\\", \\\"jsonfileloc\\\": \\\"/home/jupyter/managed_pipelines/dpm_uptick_rca/gdw-dev-dpmuptick_config.json\\\"}\"}}},\"outputs\":{\"outputFile\":\"/gcs/cjmccarthy-kfp-default-bucket/kubeflow/917089245627/mt-attr-rca-kfp-pipeline-20230207061607/virtual-component_-354102942405492736/executor_output.json\"}}",
            "--function_to_execute", "virtual_component"
        ])


@dsl.pipeline
def my_pipeline():
    op1 = comp()


if __name__ == '__main__':
    import datetime
    import warnings
    import webbrowser

    from google.cloud import aiplatform

    from kfp import compiler

    warnings.filterwarnings('ignore')
    ir_file = __file__.replace('.py', '.yaml')
    compiler.Compiler().compile(pipeline_func=my_pipeline, package_path=ir_file)
    pipeline_name = __file__.split('/')[-1].replace('_', '-').replace('.py', '')
    display_name = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
    job_id = f'{pipeline_name}-{display_name}'
    aiplatform.PipelineJob(
        template_path=ir_file,
        pipeline_root='gs://cjmccarthy-kfp-default-bucket',
        display_name=pipeline_name,
        job_id=job_id).submit()
    url = f'https://console.cloud.google.com/vertex-ai/locations/us-central1/pipelines/runs/{pipeline_name}-{display_name}?project=271009669852'
    webbrowser.open_new_tab(url)
