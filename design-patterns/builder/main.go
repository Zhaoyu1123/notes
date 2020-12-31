package main

/*
生成器是一种创建型设计模式， 使你能够分步骤创建复杂对象。

与其他创建型模式不同， 生成器不要求产品拥有通用接口。 这使得用相同的创建过程生成不同的产品成为可能。

当所需产品较为复杂且需要多个步骤才能完成时， 也可以使用生成器模式。
在这种情况下， 使用多个构造方法比仅仅使用一个复杂可怕的构造函数更简单。
分为多个步骤进行构建的潜在问题是， 构建不完整的和不稳定的产品可能会被暴露给客户端。
生成器模式能够在产品完成构建之前使其处于私密状态。

在下方的代码中， 我们可以看到 igloo­Builder冰屋生成器与 normal­Builder普通房屋生成器可建造不同类型房屋，
即 igloo冰屋和 normal­House普通房屋 。 每种房屋类型的建造步骤都是相同的。
主管 （可选） 结构体可对建造过程进行组织。
*/

import "fmt"

func main() {
	normalBuilder := getBuilder("normal")
	iglooBuilder := getBuilder("igloo")

	director := newDirector(normalBuilder)
	normalHouse := director.buildHouse()

	fmt.Printf("Normal House Door Type: %s\n", normalHouse.doorType)
	fmt.Printf("Normal House Window Type: %s\n", normalHouse.windowType)
	fmt.Printf("Normal House Num Floor: %d\n", normalHouse.floor)

	director.setBuilder(iglooBuilder)
	iglooHouse := director.buildHouse()

	fmt.Printf("\nIgloo House Door Type: %s\n", iglooHouse.doorType)
	fmt.Printf("Igloo House Window Type: %s\n", iglooHouse.windowType)
	fmt.Printf("Igloo House Num Floor: %d\n", iglooHouse.floor)

}


