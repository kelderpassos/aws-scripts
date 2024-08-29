# DynamoDB Backup Restore

Este projeto trata-se de um script para realizar a migração de tabelas do DynamoDB temporárias para outras permanentes

## O problema

O serviço AWS Backup cria cópias de tabelas e permite restaurá-las, porém impede que a escrita dos dados seja feito em tabelas já existentes, ou seja, é necessário criar novas tabelas para serem escritas. Isso se torna um problema quando há tabelas vazias que fazem parte de uma pilha (stack) do CloudFormation e elas precisam ser povoadas com estes dados.

A solução encontrada foi realizar o descarregamento das tabelas restauradas e a sequente escrita dos dados nas tabelas permanentes, tudo rodando localmente a fim de evitar problemas de limites de Lambda e custos além do estritamente necessário.

## Explicação

O arquivo main.py concentra a execução do script. Nele resgata-se as variáveis de ambientes necessárias para rodar o projeto (chaves de acesso, segredos e região da AWS) do arquivo .env para que o boto3 consiga criar uma sessão dentro da AWS, gerar um cliente e acessar os recursos necessários.

O único necessário aqui é o DynamoDB visto que a restauração do backup foi feita via console devido ao seu longo tempo de duração. O arquivo DynamoDBManager.py concenta uma classe com os métodos necessários para o descarregamento e escrita dos dados: em suma, executa-se o método scan_table do cliente em uma tabela temporária e os arquivos baixados são escritos através do método put_item.

## Execução

Para executar o serviço é necessário fazer o clone do projeto, acessar sua pasta raiz, em um terminal instalar as dependências necessárias utilizando o comando poetry install, criar e preencher um arquivo .env com as credenciais necessárias, que estão exibidas no .env.example, e roda o comando o terminal python main.py
