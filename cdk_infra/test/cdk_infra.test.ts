import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert'
import * as cdk from '@aws-cdk/core'
import * as CdkInfra from '../lib/lambda-stack'

test('Empty Stack', () => {
  const app = new cdk.App()
  // WHEN
  const stack = new CdkInfra.CdkInfraStack(app, 'MyTestStack')
  // THEN
  expectCDK(stack).to(matchTemplate({
    Resources: {}
  }, MatchStyle.EXACT))
})
