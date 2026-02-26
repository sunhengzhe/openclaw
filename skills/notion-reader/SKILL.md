---
name: notion-reading
description: Extracts and converts Notion diary content from API JSON to readable Markdown format. Use when reading personal journals, project notes, or any Notion content organized by date.
---

# Notion Reading

## Quick start

Convert Notion diary JSON to readable Markdown:

```python
# Use the conversion script
python3 notion_to_markdown.py notion_data.json
```

## When to use this skill

- Reading personal diaries from Notion
- Converting project notes to Markdown
- Processing date-organized Notion content
- Batch converting multiple Notion pages

## Conversion workflow

Copy this checklist and track progress:

```
Conversion Progress:
- [ ] Step 1: Configure API credentials
- [ ] Step 2: Fetch data from Notion API
- [ ] Step 3: Convert JSON to Markdown
- [ ] Step 4: Review and save output
```

**Step 1: Configure API credentials**

Set up your Notion integration:

1. Create integration at https://www.notion.so/my-integrations
2. Copy the "Internal Integration Token"
3. Set `NOTION_API_KEY` in config file
4. Share your Notion page with the integration

**Step 2: Fetch data from Notion API**

Use the downloader script:

```bash
python3 notion_diary_downloader.py
```

**Step 3: Convert JSON to Markdown**

The script automatically converts:

- Date headings (260101, 260102, etc.)
- Paragraph content
- Lists and other block types
- Groups content by date

**Step 4: Review and save output**

Output files:

- `notion_diary_*.json` - Original API data
- `notion_diary_*_markdown.md` - Converted Markdown

## Input format

**Notion JSON structure:**

```json
{
  "type": "heading_3",
  "heading_3": {
    "rich_text": [{"text": {"content": "260101"}}]
  }
}
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"text": {"content": "Daily content here"}}]
  }
}
```

## Output format

**Markdown structure:**

```markdown
# 📔 Notion Diary

## 260101

Daily content here

## 260102

More content...
```

## Supported block types

- Headings (heading_1, heading_2, heading_3)
- Paragraphs
- Bulleted and numbered lists
- Toggle blocks
- Callout blocks

## Configuration

### Environment variables

```bash
export NOTION_API_KEY="your_token_here"
export NOTION_PAGE_ID="your_page_id_here"
```

### Config file

Create `notion_config.json`:

```json
{
  "NOTION_API_KEY": "your_token_here",
  "NOTION_PAGE_ID": "your_page_id_here"
}
```

## Advanced usage

### Batch processing

```bash
# Process multiple pages
for page_id in "page1" "page2" "page3"; do
    sed -i "s/\"your_page_id_here\"/\"$page_id\"/" notion_config.json
    python3 notion_diary_downloader.py
done
```

### Scheduled conversion

```bash
# Add to crontab
echo "0 9 * * * $(pwd)/run_converter.sh" | crontab -
```

### Custom formatting

Modify `convert_block_to_markdown()` in `notion_to_markdown.py`:

```python
def convert_block_to_markdown(block):
    # Add custom formatting logic
    if block_type == 'heading_3':
        return f"### 📅 {text}\n"  # Add emoji
    # ...
```

## Error handling

**Common issues:**

- **401 Unauthorized**: Check API token
- **404 Not Found**: Verify page ID
- **403 Forbidden**: Ensure integration has page access
- **Connection timeout**: Check network or use proxy

## Examples

**Example 1: Basic conversion**
Input: Date heading + paragraph
Output: Structured Markdown with date section

**Example 2: Multi-day diary**
Input: Multiple date entries
Output: Chronologically organized Markdown

**Example 3: Mixed content**
Input: Various block types
Output: Properly formatted sections

## Dependencies

- Python 3.6+
- `requests` library
- Notion API access

## Testing

Run the test script:

```bash
python3 test_skill.py
```

## File structure

```
notion-reader/
├── SKILL.md                    # This file
├── notion_to_markdown.py      # Core conversion script
├── notion_diary_downloader.py  # Data fetcher
├── run_converter.sh           # Quick start script
├── example_usage.sh           # Usage examples
├── test_skill.py              # Test script
├── install.sh                 # Setup script
├── notion_config.json.template # Config template
└── .gitignore                 # Git ignore file
```
