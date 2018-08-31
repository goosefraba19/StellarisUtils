using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Stellaris.Convert
{
    public class Parser
    {
        private Lexer lexer;
        private Token token;

        public Parser(Lexer lexer)
        {
            this.lexer = lexer;
        }

        public object Parse()
        {
            this.token = this.lexer.Token();

            var pairs = new List<Tuple<string, object>>();
            while (!this.token.Type.Equals("eof"))
            {
                pairs.Add(this.ParsePair());
            }

            return this.ConvertPairs(pairs);
        }

        private Tuple<string, object> ParsePair()
        {
            if (this.token.Type.Equals("text"))
            {
                var keyOrValue = this.token.Value;

                this.token = this.lexer.Token();
                if (this.token.Type.Equals("="))
                {

                    this.token = this.lexer.Token();
                    if (this.token.Type.Equals("text"))
                    {
                        var value = this.token.Value;
                        this.token = this.lexer.Token();
                        return new Tuple<string, object>(keyOrValue, value);
                    }
                    else if (this.token.Type.Equals("{"))
                    {
                        return new Tuple<string, object>(keyOrValue, this.ParseObject());
                    }
                    else
                    {
                        throw new InvalidOperationException();
                    }

                }
                else
                {
                    return new Tuple<string, object>(null, keyOrValue);
                }
            }
            else if (this.token.Type.Equals("{"))
            {
                return new Tuple<string, object>(null, this.ParseObject());
            }
            else
            {
                throw new InvalidOperationException();
            }
        }

        private object ParseObject()
        {
            this.token = this.lexer.Token();

            var pairs = new List<Tuple<string, object>>();
            while (!this.token.Type.Equals("}"))
            {
                pairs.Add(this.ParsePair());
            }

            this.token = this.lexer.Token();

            return this.ConvertPairs(pairs);
        }

        private object ConvertPairs(List<Tuple<string, object>> pairs)
        {
            if (!pairs.Any())
            {
                return pairs;
            }

            var keySet = new HashSet<string>(pairs.Select(t => t.Item1));
            if (keySet.Count == 1 && keySet.Single() == null)
            {
                return pairs
                    .Select(t => t.Item2)
                    .ToList();
            }

            return pairs
                .GroupBy(t => t.Item1, t => t.Item2)
                .ToDictionary(
                    g => g.Key,
                    g => (g.Count() == 1) ? g.Single() : g.ToList()
                );
        }
    }
}
