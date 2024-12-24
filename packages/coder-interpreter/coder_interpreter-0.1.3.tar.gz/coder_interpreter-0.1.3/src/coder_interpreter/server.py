import asyncio
import io
import os
import subprocess
import sys

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

server = Server("coder_interpreter")


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="Creates a summary of all notes",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
        name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "summarize-notes":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="Summarize the current notes",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                         + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="code-execution",
            description="help users to do code execution, support java, python, javascript",
            inputSchema={
                "type": "object",
                "properties": {
                    "language_type": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["name", "content"],
            },
        )
    ]


def run_java(input):
    # 定义Java文件名和类名
    java_filename = 'HelloWorld.java'
    class_filename = 'HelloWorld.class'
    output = ""
    try:
        # 将Java代码写入文件
        with open('HelloWorld.java', 'w') as f:
            f.write(input)
        # 编译Java代码
        compile_process = subprocess.run(['javac', 'HelloWorld.java'], capture_output=True, text=True)
        if compile_process.returncode != 0:
            print("编译错误：")
            print(compile_process.stderr)
        else:
            # 运行Java程序
            run_process = subprocess.run(['java', 'HelloWorld'], capture_output=True, text=True)
            if run_process.returncode != 0:
                print("运行错误：")
                print(run_process.stderr)
                output = run_process.stderr
            else:
                print("Java程序输出：")
                print(run_process.stdout)
                output = run_process.stdout
    finally:
        # 删除Java源文件和生成的.class文件
        if os.path.exists(java_filename):
            os.remove(java_filename)
        if os.path.exists(class_filename):
            os.remove(class_filename)
    return output


def run_python(input):
    # 执行Python代码并捕获控制台输出
    try:
        # 创建一个StringIO对象来捕获输出
        captured_output = io.StringIO()
        sys.stdout = captured_output
        # 执行传入的Python代码
        exec(input)
        # 获取捕获的输出
        output = captured_output.getvalue()
    except Exception as e:
        output = str(e)
    finally:
        # 恢复标准输出
        sys.stdout = sys.__stdout__

    return output


def run_javascript(input):
    try:
        process = subprocess.Popen(
            ['node', '-e', input],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        output = stdout.decode() if stdout else stderr.decode()
    except Exception as e:
        output = str(e)
    return output


@server.call_tool()
async def handle_call_tool(
        name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name != "coder":
        raise ValueError(f"Unknown tool: {name}")
    if not arguments:
        raise ValueError("Missing arguments")

    language_type = arguments.get("language_type")
    content = arguments.get("content")

    if not language_type or not content:
        raise ValueError("Missing name or content")

    # 根据language_type选择执行方法
    if language_type == "java":
        output = run_java(content)
    elif language_type == "python":
        output = run_python(content)
    elif language_type == "javascript":
        output = run_javascript(content)
    else:
        raise ValueError(f"Unsupported language type: {language_type}")

    # Update server state
    notes[language_type] = content

    # Notify clients that resources have changed
    await server.request_context.session.send_resource_list_changed()

    return [
        types.TextContent(
            type="text",
            text=f"run code output: {output}",
        )
    ]


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="coder_interpreter",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
