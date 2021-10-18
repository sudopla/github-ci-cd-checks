
/**
 * CDK Util functions
 */

export const getAwsAccount = (): string => {
  if (process.env.AWS_ACCOUNT !== undefined) {
    return process.env.AWS_ACCOUNT
  } else {
    throw new Error('AWS_ACCOUNT environment variable not set. Exiting.')
  }
}

export const getAwsRegion = (): string => {
  if (process.env.AWS_REGION !== undefined) {
    return process.env.AWS_REGION
  } else {
    return 'us-east-1'
  }
}