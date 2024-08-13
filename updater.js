#!/usr/bin/env node 

'use strict';

const path = require('node:path');
const fs = require('node:fs');

function scanPkg(repositoryDir, packageName)
{
	const files = fs.readdirSync(path.join(repositoryDir, packageName, "build/pkgs")).filter((fileName) => fileName.endsWith('.json'));
	let packages = [];

	console.error(packageName);

	for (let i = 0; i < files.length; i++) {
		const file = files[i];

		console.error(file);

		packages.push(JSON.parse(fs.readFileSync(path.join(repositoryDir, packageName, "build/pkgs", file))));
	}

	return packages;
}

function scanRepo(repositoryName)
{
	const repositoryPackages = fs.readdirSync(`./${repositoryName}`);
	const packages = [];

	for (let i = 0; i < repositoryPackages.length; i++) {
		const _packages = scanPkg(repositoryName, repositoryPackages[i]);

		for (let j = 0; i < _packages.length; i++) {
			packages.push(_packages[i]);
		}
	}

	return packages;
}

function main()
{
	const repositories = ['main'];

	for (let i = 0; i < repositories.length; i++) {
		console.log(scanRepo(repositories[i]));
	}
}
main();

