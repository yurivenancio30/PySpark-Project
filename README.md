# Processando dados com o SparkOperator no Minikube

## Pré-requisitos

Certifique-se de ter instalado os seguintes requisitos antes de prosseguir:

- [Python](https://www.python.org/) (versão recomendada: 3.8)
- [Micromamba](https://mamba.readthedocs.io/) (versão recomendada: 1.4.9)
- [Docker](https://www.docker.com/) (versão recomendada: 24.0.7)
- [Docker Compose](https://docs.docker.com/compose/) (versão recomendada: v2.23.3-desktop.2)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) (versão recomendada: v1.28.2)
- [Helmfile](https://github.com/roboll/helmfile) (versão recomendada: 0.155.0)
- [Taskfile](https://taskfile.dev/) (versão recomendada: 3.22.0)

## Passo a passo para rodar o projeto

1. Clone este repositório:

   ```bash
   git clone https://github.com/yurivenancio30/PySpark-Project
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd PySpark-Project
   ```

3. Crie um ambiente virtual com o micromamba através do taskfile:

   ```bash
   task create:env
   ```

4. Suba o Mysql e o Postgres com o docker compose:

   ```bash
   docker compose up
   ```

5. Crie a tabela no Mysql:

   ```sql
   CREATE TABLE `person` ( `id`   BIGINT UNSIGNED NOT NULL   AUTO_INCREMENT, `name`  varchar(10000)  DEFAULT NULL, `age`  BIGINT UNSIGNED  DEFAULT NULL, PRIMARY KEY (`id`));
   ```

6. Aplique o helm chart para subir o operador no cluster:

   ```bash
   helmfile apply
   ```

7. Ative o ambiente virtual com o micromamba:

   ```bash
   micromamba activate spark
   ```

8. Rode o o script em python para gerar os dados fakes no mysql:

   ```bash
   task fake_data:mysql
   ```

9. Após a Criação dos dados, aplique o yaml do sparkapplication contra o cluster minikube para enviar os dados para o postgres:
   ```bash
   task apply:spark
   ```
