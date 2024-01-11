import {Body, Controller, Get, Post, Query} from '@nestjs/common';
import { ArtistsService } from './artists.service';

@Controller('artists')
export class ArtistsController {
    constructor(private readonly artistsService: ArtistsService) {}

    @Get()
    async findAll(@Query('page') page: number = 1) {
        const pageSize = 10;
        const skip = (page-1) * pageSize;

        return this.artistsService.findAll({skip, take: pageSize});
    }

    @Get("pageCount")
    async pageCount(@Query('size') size: number = 10) {
        return this.artistsService.getPageCount({size})
    }

    @Post()
    async create(@Body() body: { id: number; name: string }) {
        const { id, name } = body;
        return this.artistsService.create({ id, name });
    }

}
