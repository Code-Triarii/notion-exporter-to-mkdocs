<div align="center">
<!--
  REMEMBER THAT AT THE END OF THE MARKDOWN PAGES, THERE IS A SECTION WITH ALL THE LINKS TO BE MODIFIED OR ADDED NEW.
  This increases readability.
 -->

<!-- PROJECT LOGO -->

# 📝 Notion Wiki exporter to MkDocs

<!-- TECNOLOGIES -->

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

This project aims to provide an easy way for migrating Notion Wikis from your organization to MkDocs.
We had a use case in which we were needing to migrate all the content that we have been generating in our Notion wiki to other system/platform.
Since MkDocs is extending as powerful solution for managing wikis, we decided to give it a try thinking always with the **automation first mindset**.

[View Demo](#) · [Report Bug](https://github.com/Code-Triarii/notion-exporter-to-mkdocs/issues) · [Request Feature](https://github.com/Code-Triarii/notion-exporter-to-mkdocs/issues)

</div>

> \[!CAUTION\]
> Change description Lorem ipsum for the project information

<!-- TABLE OF CONTENTS -->

## 📚 Table of contents

- [📝 Notion Wiki exporter to MkDocs](#-notion-wiki-exporter-to-mkdocs)
  - [📚 Table of contents](#-table-of-contents)
  - [🚧 Solution Architecture](#-solution-architecture)
    - [Components](#components)
  - [🚀 Installation and Execution](#-installation-and-execution)
    - [🔨 Prerequisites](#-prerequisites)
    - [🔧 Installation](#-installation)
      - [Local environment](#local-environment)
      - [Docker environment](#docker-environment)
    - [💼 Usage](#-usage)
  - [Local development](#local-development)
  - [📍 Features and roadmap](#-features-and-roadmap)
  - [📎 Contributing](#-contributing)
  - [📃 License](#-license)
  - [👥 Contact](#-contact)
  - [References](#references)
  - [🔍 Acknowledgments](#-acknowledgments)

<!--te-->

## 🚧 Solution Architecture

> \[!IMPORTANT\]
> Do not forget to change the Architecture picture/diagram and delete the label

![Architecture](./docs/img/architecture.png)

### Components

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

## 🚀 Installation and Execution

### 🔨 Prerequisites

- Docker
- Python 3.10+

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

### 🔧 Installation

#### Local environment

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Install packages
   ```sh
   npm install
   ```
3. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

#### Docker environment

Install `Docker Engine`. Visit [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/) for more information.

1. Build docker image:

```bash
docker build . -t notion-exporter:1.0
```

2. Run docker image:

```bash
docker run -it --name notion-exporter --rm -v $(pwd):/app --user $(id -u):$(id -g) -e NOTION_TOKEN="" -e NOTION_REQUEST_WAIT_TIME="500" notion-exporter:1.0 list all -p bc3caa74-66ba-4cd1-bfcd-02f18521903e
```

> \[!TIP\]
> You can *play* with the `NOTION_REQUEST_WAIT_TIME (in ms)` value. This will set the delay in between requests to the API. Notice that Notion allows
> on average 3 requests per second by the integration. Therefore, to not get blocked the **bare minimum wait time should be 333** theoretically.

3. After the assets have been generated from Notion if everything went well, you can build the mkdocs image:

```bash
docker build .  -f Dockerfile.mkdocs -t mkdocs:1.0
```

4. Finally, you can set up you mkdocs wiki with the contents from your Notion.

```bash
docker run -d --name mkdocs -e MKDOCS_SITE="https://example.com" -e MKDOCS_PORT="8000" -e MKDOCS_INTERFACE="0.0.0.0" -e MKDOCS_SITE_NAME="mkdocs" -p 8000:8000 mkdocs:1.0
```

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

<!-- USAGE EXAMPLES -->

### 💼 Usage

______________________________________________________________________

> \[!TIP\]
> TOEDIT: Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

- CLI: In this case show the help and put some examples of the most interesting options
- Web Application: if the project is a component of a broader project, link it to the main Documentation for the project usage and especify only the specific configurations for the component. Example: if this is the front end, talk about the specific options that can be configured.

______________________________________________________________________

_For more examples, please refer to the [Documentation](https://example.com)_

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

<!-- GETTING STARTED -->

## Local development

For quick development set-up leveraging Docker, you can use the build image and run it eternally:

```bash
docker run -it --name notion-exporter --rm -v $(pwd):/app --user $(id -u):$(id -g) -e NOTION_TOKEN="" -e NOTION_REQUEST_WAIT_TIME="500" --entrypoint sh notion-exporter:1.0
```

If you need to install additional dependencies, you can access the container in a different terminal with `root` permissions:

```bash
docker exec -it -u 0:0 notion-exporter sh
```

This way you would be able to develop without having to concern about dependencies installation in your host system, testing and breaking as you like.

<!-- ROADMAP -->

## 📍 Features and roadmap

- Functionality:
- [x] Export Notion wiki.
- [x] Parametrized execution for reusability.
- [x] Indentation with 4 spaces for compatibility with [Syntax rules for python-markdown - MkDocs](https://daringfireball.net/projects/markdown/syntax#list)
- Deployment:
  - [x] Bundle automation in Docker image definition.
  - [ ] Prepare automation to deploy in kubernetes cluster with Helm.

See the [open issues](https://github.com/Code-Triarii/notion-exporter-to-mkdocs/issues) for a full list of proposed features (and known issues).

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

<!-- CONTRIBUTING -->

## 📎 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated** :chart:.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch
   ```sh
   git checkout -b feature/AmazingFeature
   ```
3. Commit your Changes
   ```sh
   git commit -m 'Add some AmazingFeature
   ```
4. Push to the Branch
   ```sh
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

<!-- LICENSE -->

## 📃 License

Distributed under the `Apache2.0` License. See [LICENSE](./LICENSE) for more information.

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

<!-- CONTACT -->

## 👥 Contact

<div align="center">

[![X](https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white)](https://twitter.com/codetriariism)
[![TikTok](https://img.shields.io/badge/TikTok-%23000000.svg?style=for-the-badge&logo=TikTok&logoColor=white)](https://www.tiktok.com/@codetriariism)
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/@codetriariism)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@CodeTriariiSM)
[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/codetriariismig/)

</div>

As we always state, our main purpose is keep learning, contributing to the community and finding ways to collaborate in interesting initiatives.
Do not hesitate to contact us at `codetriariism@gmail.com`

If you are interested in our content creation, also check our social media accounts. We have all sorts of training resources, blogs, hackathons, write-ups and more!
Do not skip it, you will like it :smirk: :smirk: :smirk: :+1:

Don't forget to give the project a star if you liked it! Thanks again! :star2: :yellow_heart:

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)

## References

- [Notion API Reference](https://developers.notion.com/reference/intro) - Giving us the details for executing the required queries.
- [Working with Notion Page content - API](https://developers.notion.com/docs/working-with-page-content)

<!-- ACKNOWLEDGMENTS -->

## 🔍 Acknowledgments

:100: :100: :100: For those that are curious about some of the resources or utilities and for sure thanking and giving credit to authors, we provide you a list of the most interesting ones (in our understanding) :100: :100: :100:

- [Notion](https://www.notion.so/c2433b9a8ff840f398c7410b3acbefd0?pvs=66)
- [MkDocs](https://www.mkdocs.org/)
- [Postman](https://www.postman.com/) - For interacting with Notion API.
- [Docker](https://www.docker.com/) - For making our work efficient.
- [Python](https://www.python.org/) - For enabling our team to produce our scripts and automations.
- [Notion SDK for Python](https://pypi.org/project/notion-client/)

[🔝 Back to top](#-notion-wiki-exporter-to-mkdocs)
