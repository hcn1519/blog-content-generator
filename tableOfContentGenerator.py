import sys
import argparse

class MarkdownListFormatter:
    def __init__(self, rawString, numberOfTopHeaderTag, postName):
        self.rawString = rawString
        
        self.numberOfHeaderTag = self.detectHeaderTag(string = rawString)
        self.titleString = MarkdownListFormatter.trimmedHeader(string = rawString, 
                                                               numberOfHeaderTag = self.numberOfHeaderTag)          
        self.numberOfTopHeaderTag = numberOfTopHeaderTag
        self.postName = postName
    
    @classmethod
    def detectHeaderTag(self, string) -> int:
        numberOfHeaderTag = 0
        for char in string:
            if char == "#":
                numberOfHeaderTag += 1
            else:
                break
        return numberOfHeaderTag

    @classmethod
    def trimmedHeader(self, string, numberOfHeaderTag) -> str:
        return string.removeprefix("#" * numberOfHeaderTag).strip()

    def formattedOrderString(self) -> str:
        tagDiff = self.numberOfHeaderTag - self.numberOfTopHeaderTag
        indent = "    " * tagDiff
        return f"{indent}1."
    
    def formattedLinkText(self) -> str:
        trimmedString = self.titleString.split(".")[-1].strip()
        return f"{self.formattedOrderString()} [{trimmedString}]"
    
    def formattedLinkURL(self) -> str:
        return self.titleString.lower().replace(" ", "-").replace(".", "")

    def formattedListString(self) -> str:
        return f"{self.formattedLinkText()}(./{self.postName}#{self.formattedLinkURL()})"

def convertToMarkdownListURL(inputs, postName):
    results = []
    numberOfTopHeaderTag = MarkdownListFormatter.detectHeaderTag(string = inputs[0])
    
    for input in inputs:
        formatter = MarkdownListFormatter(rawString = input, 
                                          numberOfTopHeaderTag = numberOfTopHeaderTag,
                                          postName = postName)
        result = formatter.formattedListString()
        results.append(result)
    return results

parser = argparse.ArgumentParser(description = "Create Table of Content list in markdown URL style")
parser.add_argument('content', nargs='+', help='content help')
parser.add_argument('--urlPrefix', 
                    metavar = 'u',
                    default = "./",
                    help = 'Prefix of URL, i.e. "./your_post_path"')

args = parser.parse_args()
inputs = args.content[0].split("\\n")
results = convertToMarkdownListURL(inputs=inputs, postName=args.urlPrefix)

print("## Table of Contents")
print()

for result in results:
    print(result)

# Usage
# python3 tableOfContentGenerator.py "## 1. What is UnitTest?\n\
# ### Solitary vs Sociable\n\
# ## 2. UnitTest의 목적\n\
# ### UseCase\n\
# ### UnitTest의 목적과 UseCase 테스트\n\
# ## 3. UnitTest에서의 테스트 대상\n\
# ### Test Isolation과 Test Double\n\
# ### Test Double\n\
# ## 4. 일반적인 UnitTest 과정" --u unittest

# Result
## Table of Contents
# 1. [What is UnitTest?](./unittest#1-what-is-unittest?)
#     1. [Solitary vs Sociable](./unittest#solitary-vs-sociable)
# 1. [UnitTest의 목적](./unittest#2-unittest의-목적)
#     1. [UseCase](./unittest#usecase)
#     1. [UnitTest의 목적과 UseCase 테스트](./unittest#unittest의-목적과-usecase-테스트)
# 1. [UnitTest에서의 테스트 대상](./unittest#3-unittest에서의-테스트-대상)
#     1. [Test Isolation과 Test Double](./unittest#test-isolation과-test-double)
#     1. [Test Double](./unittest#test-double)
# 1. [일반적인 UnitTest 과정](./unittest#4-일반적인-unittest-과정)