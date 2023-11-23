function doAction() { 
    alert("Button Clicked!");

    const AWS = require('aws-sdk');
    
    alert("1!");
    // Configure AWS SDK
    AWS.config.update({
      region: 'us-west-1',
      accessKeyId: 'AKIAWQKKSYK2JP3K7A4K',
      secretAccessKey: '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',
    });
    
    alert("2!");
    const lambda = new AWS.Lambda();
    
    alert("3!");
    const params = {
      FunctionName: 'trackstats',
      Payload: JSON.stringify({
        key1: 'value1',
        key2: 'value2',
      }),
    };
    
    alert("Lambda set up!");

    lambda.invoke(params, (err, data) => {
      if (err) {
        console.error(err);
      } else {
        const response = JSON.parse(data.Payload);
        console.log('Lambda Response:', response);
      }
    });

    alert("Lambda invoked!");
}   
