# Publisher Container
Webhook para adicionar mensagens da wppconnect na fila do RabbitMQ.
Atualizações necessarias:
	apenas concluir a inclusao na fila se;
		Contato logado é igual ao cadastrado no banco de dados (exclusivo para wppconnect)
	Alterar de funout para direct no rabbitmq e separar rotas de "onmessage" e "send-message".
