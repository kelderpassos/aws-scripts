import {
  AttributeDefinition,
  AttributeValue,
  BillingMode,
  GlobalSecondaryIndex,
  KeySchemaElement,
} from '@aws-sdk/client-dynamodb';
import { AwsCredentialIdentity } from '@aws-sdk/types';

export type TableItem = Record<string, AttributeValue>;
export type TableItems = Record<string, AttributeValue>[];

export type RoleToAssume = {
  RoleArn: string;
  RoleSessionName: string;
  DurationSeconds: number;
};

export interface Credentials extends Partial<AwsCredentialIdentity> {
  AccessKeyId: string | undefined;
  SecretAccessKey: string | undefined;
  SessionToken: string | undefined;
}

export type TableConfig = {
  TableName: string;
  KeySchema: KeySchemaElement[] | undefined;
  GlobalSecondaryIndexes: GlobalSecondaryIndex[] | undefined;
  AttributeDefinitions: AttributeDefinition[] | undefined;
  BillingMode: BillingMode | undefined;
  ProvinedThroughput?: {
    WriteCapacityUnits: number | undefined;
    ReadCapacityUnits: number | undefined;
  };
};

export interface TableMessage extends TableConfig {
  Items?: TableItems;
}

export type ExportedItems = {
  Items: TableItems;
  LastEvaluatedKey?: Record<string, AttributeValue>;
};
