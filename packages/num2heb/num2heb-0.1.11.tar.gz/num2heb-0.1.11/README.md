# num2heb

Convert numbers to Hebrew words in Python and JavaScript.

## Installation

### Python

```bash
pip install num2heb
```

### JavaScript/TypeScript

```bash
npm install num2heb
```

## Usage

### Python

```python
from num2heb import number_to_words

result = number_to_words(123)
print(result)  # Output: "מאה עשרים ושלושה"
```

### JavaScript

```javascript
const numberToWords = require("num2heb");

const result = numberToWords(123);
console.log(result); // Output: "מאה עשרים ושלושה"
```

### TypeScript

```typescript
import numberToWords from "num2heb";

const result: string = numberToWords(123);
console.log(result); // Output: "מאה עשרים ושלושה"
```

## Contributing

If you would like to contribute to this package, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
