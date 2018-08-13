using Newtonsoft.Json;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stellaris.Convert
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var inputFolderPath = args[0];
            var outputFolderPath = args[1];

            var tempFolderPath = ConfigurationManager.AppSettings["tempFolderPath"];

            var tasks = Directory.EnumerateFiles(inputFolderPath)
                .Where(p => p.EndsWith(".sav"))
                .Select(savefilePath =>
                {
                    var name = Path.GetFileNameWithoutExtension(savefilePath);
                    var extractFolderPath = Path.Combine(tempFolderPath, name);
                    var gamestatePath = Path.Combine(extractFolderPath, "gamestate");
                    var jsonPath = Path.Combine(outputFolderPath, name + ".json");
                    
                    if (File.Exists(jsonPath))
                    {
                        return null;
                    }

                    return new Task(() =>
                    {
                        var tStart = DateTime.Now;

                        if (!Directory.Exists(extractFolderPath))
                        {
                            ZipFile.ExtractToDirectory(savefilePath, extractFolderPath);
                        }
                        var text = File.ReadAllText(gamestatePath);
                        var result = new SavefileParser().Parse(text);
                        using (var writer = File.CreateText(jsonPath))
                        {
                            new JsonSerializer().Serialize(writer, result);
                        }
                        if (Directory.Exists(extractFolderPath))
                        {
                            Directory.Delete(extractFolderPath, true);
                        }

                        var tEnd = DateTime.Now;
                        var ms = (int)(tEnd - tStart).TotalMilliseconds;

                        Console.WriteLine($"{name}: {ms}");
                    });
                })
                .Where(t => t != null)
                .ToList();

            if (tasks.Any())
            {
                Console.WriteLine($"Converting {tasks.Count} files.");
                Console.WriteLine();

                Parallel.ForEach(
                    Partitioner.Create(tasks, EnumerablePartitionerOptions.NoBuffering),
                     new ParallelOptions()
                    {
                        MaxDegreeOfParallelism = 4,
                    },
                    t => t.RunSynchronously()
                );
            }
        }
    }
}
