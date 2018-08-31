using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace Stellaris.Convert
{
    public class Lexer
    {

        private readonly StreamReader reader;
        private int next;

        public Lexer(StreamReader reader)
        {
            this.reader = reader;
            this.next = this.reader.Read();
        }

        public Token Token()
        {
            while (true)
            {
                if (this.next == -1)
                {
                    return new Token("eof");
                }

                var c = (char)this.next;

                switch (c)
                {
                    case '\t':
                    case '\n':
                    case ' ':
                        this.next = this.reader.Read();
                        continue;
                    case '{':
                        this.next = this.reader.Read();
                        return new Token("{");
                    case '}':
                        this.next = this.reader.Read();
                        return new Token("}");
                    case '=':
                        this.next = this.reader.Read();
                        return new Token("=");
                    case '\"':
                        return new Token("text", this.GetEscapedString());
                }

                if (this.IsValidTextCharacter(c))
                {
                    return new Token("text", this.GetTextString(c));
                }

                throw new Exception("Could not find matching token.");
            }
        }

        private bool IsValidTextCharacter(char c)
        {
            // [a-zA-Z0-9_:.@-]
            return ('a' <= c && c <= 'z') ||
                   ('A' <= c && c <= 'Z') ||
                   ('0' <= c && c <= '9') ||
                   (c == '_') ||
                   (c == ':') ||
                   (c == '.') ||
                   (c == '@') ||
                   (c == '-');
        }

        private string GetTextString(char first)
        {
            var builder = new StringBuilder();
            builder.Append(first);

            while (true)
            {
                this.next = this.reader.Read();
                if (this.next == -1)
                {
                    throw new Exception("ERROR: EOF in GetEscapedString?");
                }

                char c = (char)this.next;
                if (this.IsValidTextCharacter(c))
                {
                    builder.Append(c);
                }
                else
                {
                    return builder.ToString();
                }
            }
        }

        private string GetEscapedString()
        {
            var builder = new StringBuilder();

            while (true)
            {
                this.next = this.reader.Read();
                if (this.next == -1)
                {
                    throw new Exception("ERROR: EOF in GetEscapedString?");
                }

                char c = (char)this.next;
                if (c == '\"')
                {
                    this.next = this.reader.Read();
                    return builder.ToString();
                }
                else
                {
                    builder.Append(c);
                }
            }
        }
    }
}
