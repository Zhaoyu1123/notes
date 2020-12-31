package main
/*
原型是一种创建型设计模式， 使你能够复制对象， 甚至是复杂对象， 而又无需使代码依赖它们所属的类。

所有的原型类都必须有一个通用的接口， 使得即使在对象所属的具体类未知的情况下也能复制对象。
原型对象可以生成自身的完整副本， 因为相同类的对象可以相互访问对方的私有成员变量。

让我们尝试通过基于操作系统文件系统的示例来理解原型模式。 操作系统的文件系统是递归的： 文件夹中包含文件和文件夹，
其中又包含文件和文件夹， 以此类推。

每个文件和文件夹都可用一个 inode接口来表示。 ​ inode接口中同样也有 clone克隆功能。

file文件和 folder文件夹结构体都实现了 print打印和 clone方法， 因为它们都是 inode类型。
同时， 注意 file和 folder中的 clone方法。 这两者的 clone方法都会返回相应文件或文件夹的副本。
同时在克隆过程中， 我们会在其名称后面添加 “_clone” 字样。
*/
import "fmt"

func main() {
	file1 := &file{name: "File1"}
	file2 := &file{name: "File2"}
	file3 := &file{name: "File3"}

	folder1 := &folder{
		childrens: []inode{file1},
		name:      "Folder1",
	}

	folder2 := &folder{
		childrens: []inode{folder1, file2, file3},
		name:      "Folder2",
	}
	fmt.Println("\nPrinting hierarchy for Folder2")
	folder2.print("  ")

	cloneFolder := folder2.clone()
	fmt.Println("\nPrinting hierarchy for clone Folder")
	cloneFolder.print("  ")
}