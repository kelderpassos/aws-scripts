import {
  SQSClient,
  SendMessageCommand,
  GetQueueUrlCommand,
} from '@aws-sdk/client-sqs';
import { randomBytes } from 'crypto';
import axios from 'axios';
import { SLACK_WEBHOOK_URL } from '../helpers/constants';

export class SqsManager {
  private readonly client: SQSClient;
  private url: string | undefined;

  constructor(
    private queueName: string,
    private region: string,
  ) {
    this.client = new SQSClient({ region: this.region });
  }

  private setQueueUrl = async () => {
    const command = new GetQueueUrlCommand({ QueueName: this.queueName });
    try {
      const { QueueUrl } = await this.client.send(command);
      this.url = QueueUrl;
    } catch (error: any) {
      await axios.post(SLACK_WEBHOOK_URL, {
        Message: `Erro ao buscar url da fila ${this.queueName}.
        Nome: ${error.name}, Erro: ${error.message}`,
      });
    }
  };

  private messageGenerator = (body: string) => {
    return {
      MessageGroupId: body,
      MessageDeduplicationId: `${body}-${Date.now()}`,
      MessageAttributes: {
        Table: {
          DataType: 'String',
          StringValue: body,
        },
      },
      MessageBody: body,
    };
  };

  public sendMessage = async (body: string) => {
    await this.setQueueUrl();

    if (!this.url) {
      throw new Error('Failed to set queue URL.');
    }

    const message = this.messageGenerator(body);
    const command = new SendMessageCommand({
      ...message,
      QueueUrl: this.url,
    });

    try {
      await this.client.send(command);
    } catch (error: any) {
      console.log('Error sending message', error);
      await axios.post(SLACK_WEBHOOK_URL, {
        Message: `Erro ao disparar mensagens.
        Nome: ${error.name}, Erro: ${error.message}`,
      });
      throw error;
    }
  };
}
