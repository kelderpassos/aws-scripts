import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
} from '@aws-sdk/client-s3';
import { SLACK_WEBHOOK_URL, generateObjectKey } from '../helpers/constants';
import axios from 'axios';

export class S3Manager {
  private readonly client: S3Client;

  constructor(private region: string) {
    this.client = new S3Client({ region: this.region });
  }

  public getObject = async (bucket: string, table: string) => {
    const params = {
      Bucket: bucket,
      Key: generateObjectKey(table),
    };

    try {
      const command = new GetObjectCommand(params);
      const result = await this.client.send(command);
      const stream = (await result.Body?.transformToString()) as string;
      const object = JSON.parse(stream);

      return object;
    } catch (error: any) {
      console.log(`Error on getting object from bucket: ${bucket}`, error);

      await axios.post(SLACK_WEBHOOK_URL, {
        Message: `Erro ao buscar objeto do bucket: ${bucket}.
        Nome: ${error.name}, Erro: ${error.message}`,
      });
      throw error;
    }
  };

  public saveItemsOnBucket = async (
    bucket: string,
    table: string,
    data: object,
  ) => {

    const params = {
      Bucket: bucket,
      Key: generateObjectKey(table),
      Body: JSON.stringify(data),
    };

    try {
      const command = new PutObjectCommand(params);
      await this.client.send(command);
    } catch (error: any) {
      console.log(`Error on saving items on bucket: ${bucket}`, error);

      await axios.post(SLACK_WEBHOOK_URL, {
        Message: `Erro ao salvar itens no bucket.
        Nome: ${error.name}, Erro: ${error.message}`,
      });
      throw error;
    }
  };
}
