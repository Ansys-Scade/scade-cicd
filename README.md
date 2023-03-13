# SCADE CICD


[![ansys-scade](https://img.shields.io/badge/Ansys-SCADE-ffb71b?labelColor=black&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC)](https://github.com/ansys-scade/)
[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Windows batch scripts to support a CICD (Continuous Integration - Continuous Delivery) workflow on a SCADE project.

The `templates` folder provides workflow templates to integrate scripts in different CICD automation servers:
  - Gitlab:
  - Jenkins:
  - GitHub:

An example is published [here](https://github.com/Ansys-Scade/scade-cicd-example) showing how to instanciate these scripts in a complete SCADE project.

## Installation

Add this repository as a subtree to your project repository using Git subtree:

    git subtree add --prefix=scade-cicd/ https://github.com/Ansys-Scade/scade-cicd.git main --squash

This command creates a subfolder `scade-cicd` in your project and pull the content of the `scade-cicd` repository inside.

It is possible to update an existing subtree with the commmand:

    git subtree pull --prefix=scade-cicd/ https://github.com/Ansys-Scade/scade-cicd.git main --squash

You can also simply copy the contain of this repository in your project within a root folder named `scade-cicd`.

## Usage

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

This project is licensed under the [MIT license](https://github.com/Ansys-Scade/scade-cicd/blob/main/LICENSE).

It makes no commercial claim over Ansys whatsoever. It extends the functionality of Ansys SCADE by adding scripts without changing the core behavior or license of the original software. The use of this project requires a legally licensed local copy of SCADE tools.

For more information on SCADE visit [Ansys Embedded SW](https://www.ansys.com/products/embedded-software).
