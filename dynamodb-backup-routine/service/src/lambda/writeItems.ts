import axios from 'axios';
import { DynamoManager } from '../dynamodb/DynamoManager';
import { BUCKET_NAME, REGION, SLACK_WEBHOOK_URL, delay } from '../helpers/constants';
import { S3Manager } from '../s3/S3Manager';
import { SQSEvent } from 'aws-lambda';

export const handler = async (event: SQSEvent): Promise<void> => {
  await delay(90000); // 1,5 minuto de espera para a exportação e provisionamento terminarem

  const tableName = event.Records[0].body;
  console.log(`Exporting items from bucket ${BUCKET_NAME}`);

  const s3 = new S3Manager(REGION);
  const dynamoDBItems = await s3.getObject(BUCKET_NAME, tableName);

  const newDynamo = new DynamoManager(REGION, undefined);
  try {
    await newDynamo.writeBackup(tableName, dynamoDBItems);
    console.log('Items written to DynamoDB!');
  } catch (error: any) {
    console.log('Error writing items to DynamoDB', error);

    await axios.post(SLACK_WEBHOOK_URL, {
      Message: `Erro em escrever itens em ${tableName}
        Nome: ${error.name}, Erro: ${error.message}`,
    });
    throw error;
  }
};
