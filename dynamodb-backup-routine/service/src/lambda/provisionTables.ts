import { StsManager } from '../sts/StsManager';
import { DynamoManager } from '../dynamodb/DynamoManager';
import { REGION, SLACK_WEBHOOK_URL, roleToAssume } from '../helpers/constants';
import { TableConfig } from '../helpers/interfaces';
import { SQSEvent } from 'aws-lambda';
import axios from 'axios';

export const handler = async (event: SQSEvent): Promise<void> => {
  const tableName = event.Records[0].body;

  const sts = new StsManager(REGION, roleToAssume);
  const credentials = await sts.assumeRole();

  const originalDynamo = new DynamoManager(REGION, credentials);
  const description = await originalDynamo.describeTable(tableName);

  const tableMessage: TableConfig = {
    TableName: description.TableName,
    KeySchema: description.KeySchema,
    GlobalSecondaryIndexes: description.GlobalSecondaryIndexes,
    AttributeDefinitions: description.AttributeDefinitions,
    BillingMode: description.BillingMode,
  };

  const newDynamo = new DynamoManager(REGION, undefined);
  try {
    await newDynamo.provisionTables(tableMessage);
    console.log(`Table ${tableName} provisioned sucessfully.`);
  } catch (error: any) {
    console.log('Error provisioning tables', error);

    await axios.post(SLACK_WEBHOOK_URL, {
      Message: `Erro em provisionar tabela ${tableName}./n
        Nome: ${error.name}, Erro: ${error.message}`,
    });
    throw error;
  }
};
