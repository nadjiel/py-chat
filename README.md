<h1 align="center">PyChat 🐍</h1>
<p align="center">Chat em linha de terminal com Sockets em Python.</p>

PyChat é um chat em linha de terminal feito em python com o intuito de praticar os conceitos de sockets e threads.

Esse projeto foi realizado como um trabalho da disciplina de Sistemas Distribuídos na faculdade de Análise de Sistemas.
Ele está bem documentado e é relativamente simples então se você quer aprender mais sobre sockets em Python recomendo dar uma olhada no código.

Foi-se estabelecido que esse chat deveria seguir um protocolo pré estabelecido de troca de mensagens.
Este protocolo está descrito melhor em sua própria seção abaixo.

## 👇 Acesso
Se quiser executar o código para experimentá-lo, pode baixar o repositório e rodar, respectivamente `server.py` e `client.py` (você vai precisar ter instalado o Python).
Note que ambos precisam de um `endereço` e `porta` onde rodar que podem ser passados por seus respectivos parâmetros, mas para saber mais sobre eles basta passar o argumento
`-h` ou `--help` quando executar qualquer um dos scripts.

## 🧾 O protocolo

### Início da conexão
A primeira mensagem que o cliente deve mandar para o servidor é:

```
!nick <seu-nick>
```

A partir daí o servidor deve responder com os usuários conectados no momento:
```
!users N user1 user2 ... userN
```

Se a primeira mensagem do cliente não for a estabelecida previamente, ele deve ser desconectado.

### Mudança de nome de usuário
Os clientes devem poder mudar seu nickname através do comando:
```
!changenickname <novo-nick>
```

O servidor deve responder a isso com a seguinte mensagem para todos os clientes conectados:
```
!changenickname <nick-antigo> <nick-novo>
```

### Cutucada
Por último, os clientes devem ser capazes de cutucar uns aos outros com:
```
!poke <usuario-a-ser-cutucado>
```

A isso o servidor deve responder para todos os usuários conectados com:
```
!poke <nick-do-cutucador> <nick-do-cutucado>
```

## ✍️ Autor
Este projeto foi feito por [@Nadjiel](https://github.com/Nadjiel).
