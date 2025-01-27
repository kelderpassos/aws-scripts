
# DynamoDB Backup Routine

Este repositório contém uma aplicação rodando na AWS que realiza o backup das informações contidas em tabelas do DynamoDB dentro do ambiente de produção numa conta separada feita especificamente para este propósito.

## Infraestrutura de pastas
O repositório conta com dois agrupamentos diferentes (infra e service), porém relacionados. Na pasta **/infra**, estão todas as estruturas e serviços necessários para que o script principal possa ser executado perfeitamente, ou seja, valores armazenados no SSM, buckets e filas necessárias são configurados neste primeiro agrupamento e utilizados no segundo.

A pasta **service** contém as lambdas responsáveis por executar toda a rotina de backup. As únicas configurações existentes no serverless são os papeis (roles), com suas respectivas políticas e permissões, que cada lambda irá assumir.

Já a pasta **/service/src** contém os SDKs utilizados para manipular os recursos da AWS envolvidos no processo de backup. Cada SDK com seus métodos está organizado em classes e pastas nomeadas de acordo com o serviço.

## Fluxo de execução
A aplicação é executada por quatro lambdas diferentes. A primeira está no arquivo trigger.ts e executa as demais. Seu principal propósito é ser executada de acordo com o evento determinado no serverless.yml, extrair os nomes das tabelas do DynamoDB vindo do ambiente de produção a partir de um AssumeRole e disparar filas pra cada lambda subsequente.

As lambdas seguintes executam os procedimentos descritos em seu nome: exportam os itens do DynamoDB para o S3 da conta de backup, provisiona as tabelas que não existem na conta de backup e escreve os itens no DynamoDB da conta de backup através dos dados presentes no S3 e escritos pela primeira lambda.

## Implementação
Para subir toda a aplicação, é necessário rodar o arquivo backup-script.sh que contém um script em bash que irá acessar cada pasta e realizar as respectivas implementações de cada arquivo serverless.yml

Comando: `bash backup-script.sh backup`

Cabe destacar que o termo **backup** corresponde ao ambiente onde a aplicação será executada. Esse parâmetro é obrigatório e pode ser substituído por outro valor que corresponda a algum outro ambiente a ser criado dentro da conta de backup.