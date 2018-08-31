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
            this.Step();
        }

        private HashSet<char> textSet = new HashSet<char>("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:.@-".ToCharArray());

        public Token Token()
        {
            while (true)
            {
                var i = this.next;
                if (i == -1)
                {
                    return new Token("eof");
                }

                var c = (char)this.next;

                switch (c)
                {
                    case '\t':
                    case '\n':
                    case ' ':
                        this.Step();
                        continue;
                    case '{':
                        this.Step();
                        return new Token("{");
                    case '}':
                        this.Step();
                        return new Token("}");
                    case '=':
                        this.Step();
                        return new Token("=");
                }

                if (c == '\"')
                {
                    return new Token("text", this.GetEscapedString());
                }

                if (this.textSet.Contains(c))
                {
                    return new Token("text", this.GetTextString(c));
                }

                throw new Exception("Could not find matching token.");
            }
        }

        private int Step()
        {
            this.next = this.reader.Read();
            return this.next;
        }

        private string GetTextString(char first)
        {
            var builder = new StringBuilder();
            builder.Append(first);

            while (true)
            {
                var i = this.Step();
                if (i == -1)
                {
                    throw new Exception("ERROR: EOF in GetEscapedString?");
                }

                char c = (char)i;
                if (this.textSet.Contains(c))
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
                var i = this.Step();
                if (i == -1)
                {
                    throw new Exception("ERROR: EOF in GetEscapedString?");
                }

                char c = (char)i;
                if (c == '\"')
                {
                    this.Step();
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
