import {Body, Controller, Get, Post, Query} from '@nestjs/common';
import { LabelsService } from './labels.service';

@Controller('labels')
export class LabelsController {
    constructor(private readonly labelsService: LabelsService) {}

    @Get()
    async findAll(@Query('page') page: number = 1) {
        const pageSize = 10;
        const skip = (page-1) * pageSize;

        return this.labelsService.findAll({skip, take: pageSize});
    }

    @Get("pageCount")
    async pageCount(@Query('size') size: number = 10) {
        return this.labelsService.getPageCount({size})
    }

    @Post()
      async create(@Body() body: { id: number; name: string; company_name: string }) {
        const { id, name, company_name } = body;
        return this.labelsService.create({ id, name, company_name });
      }
}
