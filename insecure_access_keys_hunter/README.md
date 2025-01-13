# README: Insecure Access Key Hunter

## Descrição do Projeto

O **Insecure Access Key Hunter** é um script Python que automatiza a identificação e exclusão de chaves de acesso antigas e desnecessárias de usuários IAM na AWS. Ele é útil para ajudar a melhorar a segurança ao garantir que chaves de acesso não utilizadas ou muito antigas sejam removidas, reduzindo o risco de exploração indevida.

### Funcionalidades

- Lista usuários e suas chaves de acesso vinculadas.
- Identifica chaves de acesso mais antigas que um período especificado (em dias).
- Gera um relatório detalhado em formato CSV com as chaves identificadas.
- Permite a exclusão opcional das chaves antigas, conforme a confirmação do usuário.

---

## Requisitos

### Pré-requisitos

- **Python 3.9+**
- **Credenciais AWS** configuradas no arquivo `~/.aws/credentials`.
- Permissões adequadas para o perfil IAM utilizado:
  - `iam:ListUsers`
  - `iam:ListAccessKeys`
  - `iam:DeleteAccessKey` (se a exclusão for realizada)

### Bibliotecas Necessárias

Este projeto utiliza o gerenciador de pacotes **uv**, uma alternativa moderna e rápida ao pip. Caso você ainda não tenha o uv instalado, siga as instruções abaixo:

```
pip install uv
```
Ou, para sistemas Unix, usando o instalador oficial:


```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


## Como Usar

### 1. Configuração do Ambiente

Certifique-se de que o arquivo de credenciais AWS (`~/.aws/credentials`) está configurado corretamente. Ele deve conter os perfis AWS que você deseja utilizar, com formato semelhante ao exemplo abaixo:

```ini
[default]
aws_access_key_id = SUA_ACCESS_KEY_ID
aws_secret_access_key = SUA_SECRET_ACCESS_KEY

[seu-perfil]
aws_access_key_id = OUTRA_ACCESS_KEY_ID
aws_secret_access_key = OUTRA_SECRET_ACCESS_KEY
```

### 2. Execução do Script

Execute o script diretamente no terminal:

```bash
uv run ./src/main.py
```
Este comando instalará automaticamente as dependências necessárias para o projeto e o executará.

### 3. Passos Interativos

Durante a execução, o script solicita as seguintes informações:

1. **Seleção do Perfil AWS:** Uma lista de perfis será exibida. Escolha o número correspondente ao perfil desejado.
2. **Idade das Chaves:** Insira o limite de idade (em dias) para considerar uma chave como "antiga".
3. O script exibirá as chaves encontradas mais antigas que o limite especificado e perguntará se deseja excluí-las.

### 4. Relatório Gerado

Um relatório em formato CSV será gerado no diretório de execução com informações detalhadas sobre as chaves encontradas. O nome do arquivo segue o formato:

```text
report-{nome-do-perfil}.csv
```

---

## Estrutura do Código

- **`IamManager`**: Classe responsável por interagir com o serviço AWS IAM, listar usuários e chaves, além de excluir chaves.
- **Funções principais**:
  - `access_key_scan`: Obtém os dados de entrada do usuário.
  - `get_old_keys`: Identifica as chaves mais antigas que o limite definido.
  - `generate_report`: Gera o relatório CSV com as chaves identificadas.
  - `get_delete_reply`: Confirma a exclusão das chaves.

---

## Exemplo de Uso

### Cenário

- Você quer verificar chaves antigas de 90 dias associadas ao perfil `default`.
- Deseja excluir as chaves encontradas.

### Fluxo

1. Execute o script.
2. Escolha o perfil `default`.
3. Insira `90` como limite de idade.
4. Revise as informações exibidas.
5. Escolha `1` para confirmar a exclusão.

O script então:

- Gera um relatório `report-default.csv`.
- Exclui as chaves antigas.

---

## Considerações de Segurança

- **Cuidado ao excluir chaves**: A exclusão de chaves de acesso não pode ser desfeita. Certifique-se de que os usuários afetados não dependem mais dessas chaves antes de prosseguir.
- **Gerenciamento de Credenciais**: Utilize perfis AWS com permissões mínimas necessárias para evitar exposição indevida.

---

## Debug e Logs

O script utiliza o módulo `logging` para registrar erros e informações importantes. Verifique os logs no terminal caso encontre problemas durante a execução.

---

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.