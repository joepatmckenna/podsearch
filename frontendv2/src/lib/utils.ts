export const zip = (rows) => rows[0].map((_, c) => rows.map((row) => row[c]));

export const argmax = (arr) => {
  if (arr.length === 0) {
    return -1;
  }

  let max = arr[0];
  let maxIndex = 0;

  for (let i = 1; i < arr.length; i++) {
    if (arr[i] > max) {
      maxIndex = i;
      max = arr[i];
    }
  }

  return maxIndex;
};

export const argsort = (arr) => {
  return arr
    .map((v, i) => [v, i])
    .sort((v1, v2) => parseInt(v1) - parseInt(v2))
    .map((vi) => vi[1]);
};

export const sum = (x) => x.reduce((agg, xi) => agg + xi, 0);
