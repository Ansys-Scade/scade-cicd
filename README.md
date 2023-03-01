# SCADE CICD

Windows batch scripts to support a CICD (Continuous Integration - Continuous Delivery) workflow on a SCADE project.

The `templates` folder provides workflow templates to integrate scripts in different CICD automation servers:
    - Gitlab:
    - Jenkins:
    - GitHub:

## How to install

Add this repository as a subtree to your project repository using Git subtree:

    git subtree add --prefix=scade-cicd/ https://github.com/Ansys-Scade/scade-cicd.git main --squash

This command creates a subfolder `scade-cicd` in your project and pull the content of the `scade-cicd` repository inside.

It is possible to update an existing subtree with the commmand:

    git subtree pull --prefix=scade-cicd/ https://github.com/Ansys-Scade/scade-cicd.git main --squash

You can also simply copy the contain of this repository in your project within a root folder named `scade-cicd`.

## How to use

### GitHub
Copy the folder `scade-cicd\templates\.github` at the root of your GitHub project repository.
In this folder, edit the file `.github\workflows\scade.yml` to configure project settings in the `env` section:
  - set the path to the SCADE installation folder on your GitHub runner
  - set the path to the different SCADE projects etp files (without the `.etp` extension)
  - set configurations names for the different SCADE activities

Make additional change to adapt this newly configured GitHub workflow to your specific repository needs: e.g. run only when commit to the main branch, ...

### GitLab
Create a file `.gitlab-ci.yml` at the root of your GitHub project repository.

Edit this file to configure project settings:
  - set the path to the SCADE installation folder on your GitLab runner
  - set the path to the different SCADE projects etp files (without the `.etp` extension)
  - set configurations names for the different SCADE activities

Example of content:

    include:
    - local: '/scade-cicd/templates/.gitlab-ci-template.yml'

    variables:
        # SCADE installation folder for runners
        SCADE_DIR: "C:\\Program Files\\ANSYS Inc\\v231\\SCADE"
        # SCADE project relative path without extension
        SCADE_PROJECT_ROOT: "CruiseControl\\CruiseControl"
        # SCADE test project relative path without extension
        SCADE_PROJECT_TEST_ROOT: "CruiseControl_Test\\CruiseControl_Test"
        # SCADE test result project relative path without extension
        SCADE_PROJECT_TEST_RESULT_ROOT: "CruiseControl_Test\\CruiseControl_Test"
        CONF_CHECK: "KCG"
        CONF_REPORT: "RTF"
        CONF_GEN: "KCG"
        CONF_TEST: "Test"

### Jenkins
Copy the file `scade-cicd\templates\Jenkinsfile` at the root of your GitHub project repository.
Edit this file to configure project settings in the `pipeline/environment` section:
  - set the path to the SCADE installation folder on your Jenkins agent
  - set the path to the different SCADE projects etp files (without the `.etp` extension)
  - set configurations names for the different SCADE activities
  - adapt path to artifacts to upload

Make additional change to adapt this newly configured GitHub workflow to your specific repository needs: e.g. run only when commit to the main branch, ...

## License and acknowledgments

This project is licensed under the `MIT license`.

It makes no commercial claim over Ansys whatsoever. It extends the functionality of Ansys SCADE by adding scripts without changing the core behavior or license of the original software. The use of this project requires a legally licensed local copy of SCADE tools.

For more information on SCADE, see the Ansys Embedded SW page on the Ansys website (https://www.ansys.com/products/embedded-software).
