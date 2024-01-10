import { Injectable } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class ArtistsService {
    private prisma = new PrismaClient();

    async findAll({skip = 0, take = 10}: { skip?: number; take?: number } = {}): Promise<any[]> {
        return this.prisma.artists.findMany({
            skip,
            take,
        });
    }

    async getPageCount({size = 10}): Promise<any> {
        return Math.ceil((await this.prisma.artists.count()) / size);
    }
}
