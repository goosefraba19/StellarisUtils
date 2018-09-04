using Newtonsoft.Json;
using System;
using System.IO;
using System.IO.Compression;
using System.Linq;

namespace Stellaris.Convert
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var tStart = DateTime.Now;

            var obj = ReadAndParseSaveObject(args[0]);

            var tParse = DateTime.Now;

            WriteSaveObject(obj, args[1]);

            var tEnd = DateTime.Now;

            var msRead = (tParse - tStart).TotalMilliseconds;
            var msWrite = (tEnd - tParse).TotalMilliseconds;
            Console.WriteLine($"{msRead}, {msWrite}");
        }

        private static object ReadAndParseSaveObject(string filePath)
        {
            using (var archive = ZipFile.Open(filePath, ZipArchiveMode.Read))
            {
                var entry = archive.GetEntry("gamestate");

                using (var stream = entry.Open())
                using (var buffered = new BufferedStream(stream))
                using (var reader = new StreamReader(buffered))
                {
                    var lexer = new Lexer(reader);
                    var parser = new Parser(lexer);

                    return parser.Parse();
                }
            }
        }

        private static void WriteSaveObject(object obj, string filePath)
        {
            if (File.Exists(filePath))
            {
                File.Delete(filePath);
            }

            using (var archive = ZipFile.Open(filePath, ZipArchiveMode.Create))
            {
                var entry = archive.CreateEntry("gamestate.json", CompressionLevel.Optimal);

                using (var writer = new StreamWriter(entry.Open()))
                {
                    new JsonSerializer().Serialize(writer, obj);
                }
            }
        }
    }
}
