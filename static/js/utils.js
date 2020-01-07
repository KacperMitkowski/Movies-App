export {utils}

const utils = {
  getComment: function (receivedData) {
    if (receivedData === null)
      return 'No data';
    else
      return receivedData;
  }
};