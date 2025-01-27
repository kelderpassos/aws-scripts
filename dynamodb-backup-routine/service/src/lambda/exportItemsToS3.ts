import { StsManager } from '../sts/StsManager';
import { S3Manager } from '../s3/S3Manager';
import { DynamoManager } from '../dynamodb/DynamoManager';
import {
  BUCKET_NAME,
  REGION,
  SLACK_WEBHOOK_URL,
  roleToAssume,
} from '../helpers/constants';
import { SQSEvent } from 'aws-lambda';
import axios from 'axios';

export const handler = async (event: SQSEvent): Promise<void> => {
  const tableName = event.Records[0].body;
  console.log(`Exporting items from ${tableName}`);

  const sts = new StsManager(REGION, roleToAssume);
  const credentials = await sts.assumeRole();

  const originalDynamo = new DynamoManager(REGION, credentials);
  const { Items } = await originalDynamo.exportItems(tableName, undefined);

  const s3 = new S3Manager(REGION);
  try {
    await s3.saveItemsOnBucket(BUCKET_NAME, tableName, Items);
    console.log(`Items saved on bucket: ${BUCKET_NAME}`);
  } catch (error: any) {
    console.log(`Error on saving items on bucket ${BUCKET_NAME}`, error);

    await axios.post(SLACK_WEBHOOK_URL, {
      Message: `Erro ao salvar no bucket ${BUCKET_NAME}
        Nome: ${error.name}, Erro: ${error.message}`,
    });
    throw error;
  }
};
