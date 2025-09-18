import { downloadSourceSchema } from './schemas';
import * as fs from 'fs'

//const fileToTest = '../hydra-skidrowreloaded/skidrow_cleaned.json'
const fileToTest = '../hydra-kevin/combined.json'
const rawData = fs.readFileSync(fileToTest, 'utf-8');
const jsonData = JSON.parse(rawData);

try
{
  downloadSourceSchema.parse(jsonData);
  console.log('Valid JSON!');
} 
catch (e)
{
    // Check if the error is a ZodError
    if (e instanceof Error && 'errors' in e)
    {
        console.error('Invalid JSON: ', (e as any).errors);
    }
    else
    {
        console.error('Unexpected error:', e);
    }
}
