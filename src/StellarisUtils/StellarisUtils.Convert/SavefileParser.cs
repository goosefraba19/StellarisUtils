using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Text.RegularExpressions;

namespace Stellaris.Convert
{
    public class SavefileParser
    {
        public object Parse(string text)
        {
            var stream = new TokenStream(text);

            var attrs = new List<KeyValuePair<string, object>>();
            while (stream.Current.Type != TokenType.EndOfFile) {
                attrs.Add(this.ParseAttr(stream));
            }

            return ConvertAttrs(attrs);
        }

        private KeyValuePair<string, object> ParseAttr(TokenStream stream)
        {
            if (stream.Current.Type == TokenType.Text)
            {
                var keyOrValue = stream.Current.Value;
                stream.Step();
                if (stream.Current.Type == TokenType.Equals)
                {
                    stream.Step();
                    if (stream.Current.Type == TokenType.Text)
                    {
                        var value = stream.Current.Value;
                        stream.Step();
                        return new KeyValuePair<string, object>(keyOrValue, value);
                    }
                    else if (stream.Current.Type == TokenType.CurlyOpen)
                    {
                        return new KeyValuePair<string, object>(
                            keyOrValue,
                            this.ParseObject(stream)
                        );
                    }
                    else
                    {
                        throw new InvalidOperationException();
                    }
                }
                else
                {
                    return new KeyValuePair<string, object>(
                        null,
                        keyOrValue
                    );
                }
            }
            else if (stream.Current.Type == TokenType.CurlyOpen)
            {
                return new KeyValuePair<string, object>(
                    null,
                    this.ParseObject(stream)
                );
            }
            else
            {
                throw new InvalidOperationException();
            }
        }

        private object ParseObject(TokenStream stream)
        {
            if (stream.Current.Type != TokenType.CurlyOpen)
            {
                throw new ArgumentException();
            }

            stream.Step();

            var result = new List<KeyValuePair<string, object>>();

            while (stream.Current.Type != TokenType.CurlyClose)
            {
                result.Add(this.ParseAttr(stream));
            }

            stream.Step();

            return ConvertAttrs(result);
        }

        private object ConvertAttrs(List<KeyValuePair<string, object>> attrs)
        {
            if (attrs.All(p => p.Key == null))
            {
                return attrs.Select(p => p.Value).ToList();
            }
            else
            {
                var result = new Dictionary<string, object>();

                foreach (var group in attrs.GroupBy(a => a.Key))
                {
                    if (group.Count() == 1)
                    {
                        var pair = group.Single();
                        result.Add(pair.Key, pair.Value);
                    }
                    else
                    {
                        result.Add(
                            group.Key, 
                            group.Select(p => p.Value).ToList()
                        );
                    }
                }

                return result;
            }
        }

        private class TokenStream
        {

            private List<Pattern> patterns = new List<Pattern>()
            {
                new Pattern(TokenType.Whitespace, new Regex("\\G\\s+")),
                new Pattern(TokenType.Text, new Regex("\\G[a-zA-Z0-9_:.-]+")),
                new Pattern(TokenType.Text, new Regex("\\G\"([^\"]*)\"")),
                new Pattern(TokenType.Equals, new Regex("\\G=")),
                new Pattern(TokenType.CurlyOpen, new Regex("\\G{")),
                new Pattern(TokenType.CurlyClose, new Regex("\\G}")),
            };

            public Token Current { get; private set; }

            private readonly string text;
            private int index = 0;

            public TokenStream(string text) 
            {
                this.text = text;
                this.Step();
            }

            public void Step()
            {
                while (index < text.Length)
                {
                    var tokens = this.patterns
                        .Select(p => new { Pattern = p, Match = p.Regex.Match(text, index) })
                        .Where(a => a.Match.Success)
                        .Select(a => new Token()
                        {
                            Type = a.Pattern.Type,
                            Value = a.Match.Groups[a.Match.Groups.Count - 1].Value,
                            Length = a.Match.Length
                        })
                        .ToList();

                    if (tokens.Any())
                    {
                        var result = tokens
                           .OrderByDescending(t => t.Length)
                           .First();

                        index += result.Length;

                        if (result.Type != TokenType.Whitespace)
                        {
                            this.Current = result;
                            return;
                        }
                    }
                    else
                    {
                        throw new InvalidOperationException("Could not generate token.");
                    }
                }

                this.Current = new Token()
                {
                    Type = TokenType.EndOfFile,
                    Value = string.Empty,
                    Length = 0,
                };
                return;
            }

            private class Pattern
            {
                public TokenType Type { get; set; }
                public Regex Regex { get; set; }

                public Pattern(TokenType type, Regex regex)
                {
                    this.Type = type;
                    this.Regex = regex;
                }
            }
        }


        private struct Token
        {
            public TokenType Type { get; set; }
            public string Value { get; set; }
            public int Length { get; set; }
        }

        private enum TokenType
        {
            Undefined = 0,
            Whitespace,
            Text,
            Equals,
            CurlyOpen,
            CurlyClose,
            EndOfFile
        }

    }
}
