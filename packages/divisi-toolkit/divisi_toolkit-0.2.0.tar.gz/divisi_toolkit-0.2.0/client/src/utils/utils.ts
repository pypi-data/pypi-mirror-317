import type {
  Slice,
  SliceFeature,
  SliceFeatureAnd,
  SliceFeatureBase,
  SliceFeatureNegation,
  SliceFeatureOr,
} from './slice.type';

export function sliceToString(slice: Slice): string {
  let featureKeys = Object.keys(slice.featureValues);
  featureKeys.sort();
  return featureKeys.map((k) => `${k}: ${slice.featureValues[k]}`).join(',');
}

export let areSetsEqual = <T>(a: Set<T>, b: Set<T>): boolean =>
  a.size === b.size && [...a].every((value) => b.has(value));

export function areObjectsEqual(x, y) {
  if (x === y) return true;
  // if both x and y are null or undefined and exactly the same

  if (!(x instanceof Object) || !(y instanceof Object)) return false;
  // if they are not strictly equal, they both need to be Objects

  if (x.constructor !== y.constructor) return false;
  // they must have the exact same prototype chain, the closest we can do is
  // test there constructor.

  for (var p in x) {
    if (!x.hasOwnProperty(p)) continue;
    // other properties were tested using x.constructor === y.constructor

    if (!y.hasOwnProperty(p)) return false;
    // allows to compare x[ p ] and y[ p ] when set to undefined

    if (x[p] === y[p]) continue;
    // if they have the same strict value or identity then they are equal

    if (typeof x[p] !== 'object') return false;
    // Numbers, Strings, Functions, Booleans must be strictly equal

    if (!areObjectsEqual(x[p], y[p])) return false;
    // Objects and Arrays must be tested recursively
  }

  for (p in y) if (y.hasOwnProperty(p) && !x.hasOwnProperty(p)) return false;
  // allows x[ p ] to be set to undefined

  return true;
}

export function cumulativeSum(arr: Array<number>): Array<number> {
  return arr.map(
    (
      (sum) => (value) =>
        (sum += value)
    )(0)
  );
}

// return a copy of featureToCopy that has an identical tree to referenceFeature,
// where instances of searchFeature will be replaced with replaceFeature
export function withToggledFeature(
  featureToCopy: SliceFeatureBase,
  referenceFeature: SliceFeatureBase,
  searchFeature: SliceFeatureBase,
  replaceFeature: SliceFeatureBase = null
): SliceFeatureBase {
  if (areObjectsEqual(searchFeature, referenceFeature)) {
    if (replaceFeature == null) {
      if (areObjectsEqual(searchFeature, featureToCopy))
        return { type: 'base' };
      return Object.assign({}, referenceFeature);
    }
    return replaceFeature;
  }
  let copied = Object.assign({}, featureToCopy);
  if (referenceFeature.type == 'negation') {
    (copied as SliceFeatureNegation).feature = withToggledFeature(
      (copied as SliceFeatureNegation).feature,
      (referenceFeature as SliceFeatureNegation).feature,
      searchFeature,
      replaceFeature
    );
  } else if (referenceFeature.type == 'and') {
    (copied as SliceFeatureAnd).lhs = withToggledFeature(
      (copied as SliceFeatureAnd).lhs,
      (referenceFeature as SliceFeatureAnd).lhs,
      searchFeature,
      replaceFeature
    );
    (copied as SliceFeatureAnd).rhs = withToggledFeature(
      (copied as SliceFeatureAnd).rhs,
      (referenceFeature as SliceFeatureAnd).rhs,
      searchFeature,
      replaceFeature
    );
  } else if (referenceFeature.type == 'or') {
    (copied as SliceFeatureOr).lhs = withToggledFeature(
      (copied as SliceFeatureOr).lhs,
      (referenceFeature as SliceFeatureOr).lhs,
      searchFeature,
      replaceFeature
    );
    (copied as SliceFeatureOr).rhs = withToggledFeature(
      (copied as SliceFeatureOr).rhs,
      (referenceFeature as SliceFeatureOr).rhs,
      searchFeature,
      replaceFeature
    );
  }
  return copied;
}

export function featureNeedsParentheses(
  feature: SliceFeatureBase,
  parent: SliceFeatureBase = null
): boolean {
  if (feature.type == 'and' || feature.type == 'or') {
    if (parent.type == 'and' || parent.type == 'or') {
      return feature.type != parent.type;
    }
    if (parent.type == 'negation') return true;
  }
  return false;
}

// returns true if the two features have the same structure except for some
// features being substituted by an empty SliceFeatureBase
export function featuresHaveSameTree(
  feature: SliceFeatureBase,
  otherFeature: SliceFeatureBase,
  allowValueDifferences: boolean = false
): boolean {
  if (feature.type != otherFeature.type) {
    return feature.type == 'base' || otherFeature.type == 'base';
  }
  if (feature.type == 'feature') {
    if (allowValueDifferences)
      return (
        otherFeature.type == 'feature' &&
        (feature as SliceFeature).col == (otherFeature as SliceFeature).col
      );
    return areObjectsEqual(feature, otherFeature);
  }
  if (feature.type == 'negation') {
    return featuresHaveSameTree(
      (feature as SliceFeatureNegation).feature,
      (otherFeature as SliceFeatureNegation).feature,
      allowValueDifferences
    );
  }
  if (feature.type == 'and' || feature.type == 'or') {
    return (
      featuresHaveSameTree(
        (feature as SliceFeatureAnd).lhs,
        (otherFeature as SliceFeatureAnd).lhs,
        allowValueDifferences
      ) &&
      featuresHaveSameTree(
        (feature as SliceFeatureAnd).rhs,
        (otherFeature as SliceFeatureAnd).rhs,
        allowValueDifferences
      )
    );
  }
  return true;
}

export function createWebWorker(script: string): {
  worker: Worker;
  url: string;
} {
  // serve it ourselves as a blob
  let blob = new Blob([script], {
    type: 'text/javascript',
  });

  let url = window.URL.createObjectURL(blob);
  return {
    worker: new Worker(url, { type: 'module' }),
    url,
  };
}

const prefixMetrics = ['count'];

export function sortMetrics(a: string, b: string): number {
  if (prefixMetrics.includes(a.toLocaleLowerCase())) {
    if (prefixMetrics.includes(b.toLocaleLowerCase()))
      return a.localeCompare(b);
    else return -1;
  } else if (prefixMetrics.includes(b.toLocaleLowerCase())) return 1;
  return a.localeCompare(b);
}

export function shuffle<T>(array: T[]): T[] {
  var currentIndex = array.length,
    temporaryValue,
    randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

export function randomStringRep(): string {
  return `custom-${new Array(20)
    .fill(0)
    .map((_) => Math.floor(Math.random() * 10))
    .join('')}`;
}
